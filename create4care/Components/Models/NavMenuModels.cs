using Microsoft.AspNetCore.Components;

namespace create4care.Components.Models;

public class NavItem
{
    public string Name { get; set; }
    public string Href { get; set; }
    public RenderFragment Icon { get; set; }
}

public class MenuSection
{
    public string Header { get; set; }
    public List<NavItem> NavItems { get; set; }
}

public class NavMenuModel
{
    public List<MenuSection> MenuSections { get; set; }
}