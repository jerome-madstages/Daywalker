#include "DaywalkerAgentComponent.h"
#include "HttpModule.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonWriter.h"

void UDaywalkerAgentComponent::QueryLLM(const FString& Prompt, int32 MaxTokens)
{
    FHttpModule* Http = &FHttpModule::Get();
    TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

    Request->OnProcessRequestComplete().BindUObject(this, &UDaywalkerAgentComponent::HandleResponse);
    Request->SetURL(ServerURL + TEXT("/v1/completions"));
    Request->SetVerb(TEXT("POST"));
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

    // Build JSON body: {"model":"local","prompt":"...","max_tokens":128}
    TSharedRef<FJsonObject> Root = MakeShared<FJsonObject>();
    Root->SetStringField(TEXT("model"), ModelName);
    Root->SetStringField(TEXT("prompt"), Prompt);
    Root->SetNumberField(TEXT("max_tokens"), MaxTokens);

    FString Body;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&Body);
    FJsonSerializer::Serialize(Root, Writer);
    Request->SetContentAsString(Body);

    Request->ProcessRequest();
}

void UDaywalkerAgentComponent::HandleResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
{
    FString TextOut;

    if (bWasSuccessful && Response.IsValid() && EHttpResponseCodes::IsOk(Response->GetResponseCode()))
    {
        // Parse {"choices":[{"text":"..."}]}
        TSharedPtr<FJsonObject> Json;
        const FString Payload = Response->GetContentAsString();
        TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Payload);
        if (FJsonSerializer::Deserialize(Reader, Json) && Json.IsValid())
        {
            const TArray<TSharedPtr<FJsonValue>>* Choices = nullptr;
            if (Json->TryGetArrayField(TEXT("choices"), Choices) && Choices && Choices->Num() > 0)
            {
                const TSharedPtr<FJsonObject> First = (*Choices)[0]->AsObject();
                if (First.IsValid())
                {
                    FString Text;
                    if (First->TryGetStringField(TEXT("text"), Text))
                    {
                        TextOut = Text;
                    }
                }
            }
        }
    }
    else
    {
        const int32 Code = (Response.IsValid() ? Response->GetResponseCode() : -1);
        TextOut = FString::Printf(TEXT("[Daywalker] HTTP %d (success=%s)"), Code, bWasSuccessful ? TEXT("true") : TEXT("false"));
    }

    OnReply.Broadcast(TextOut);
}
