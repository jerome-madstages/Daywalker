using UnrealBuildTool;

public class Daywalker : ModuleRules
{
    public Daywalker(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(
            new string[] { "Core","CoreUObject","Engine","HTTP","Json","JsonUtilities" }
        );
    }
}
