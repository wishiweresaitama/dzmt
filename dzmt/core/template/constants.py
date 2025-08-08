CONFIG_CPP_CONTENT = """\
class CfgMods
{
    class {{name}}
    {
        name = "{{name}}";
        dir = "{{name}}";
        credits = "";
        author = "{{author}}";
        creditsJson = "";
        versionPath = "";
        inputs = "";
        type = "mod";
        dependencies[] = {
            "Game",
            "World",
            "Mission",
        };
        class defs
        {
            class imageSets
            {
                files[] = {};
            };

            class gameScriptModule
            {
                value = "";
                files[] = 
                {
                    "{{prefix}}/Scripts/3_Game"
                };
            };

            class worldScriptModule
            {
                value = "";
                files[] = 
                {
                    "{{prefix}}/Scripts/4_World"
                };
            };

            class missionScriptModule
            {
                value = "";
                files[] = 
                {
                    "{{prefix}}/Scripts/5_Mission"
                };
            };
        };
    };
};
"""
