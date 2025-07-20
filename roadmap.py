from agents import function_tool

@function_tool
def get_career_roadmap(field: str) -> str:
    maps = {
        "Software engineer" "learn python , Htm, Css, Tailwind CSS"
    }
    return maps.get(field.lower(),"no road map found for that field")