#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "DaywalkerAgentComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FDaywalkerReplySignature, const FString&, ResponseText);

UCLASS(ClassGroup=(Daywalker), meta=(BlueprintSpawnableComponent))
class DAYWALKER_API UDaywalkerAgentComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Daywalker")
    FString ServerURL = TEXT("http://127.0.0.1:8080");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Daywalker")
    FString ModelName = TEXT("local");

    UPROPERTY(BlueprintAssignable, Category="Daywalker")
    FDaywalkerReplySignature OnReply;

    UFUNCTION(BlueprintCallable, Category="Daywalker")
    void QueryLLM(const FString& Prompt, int32 MaxTokens = 128);

private:
    void HandleResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful);
};
