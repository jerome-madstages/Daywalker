#include "Modules/ModuleManager.h"

class FDaywalkerModule : public IModuleInterface
{
public:
    virtual void StartupModule() override {}
    virtual void ShutdownModule() override {}
};

IMPLEMENT_MODULE(FDaywalkerModule, Daywalker)
