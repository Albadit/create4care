using Microsoft.AspNetCore.Components;

namespace create4care.Components.Models;

public class NavItem
{
    public required string Name { get; set; }
    public required string Href { get; set; }
    public required RenderFragment Icon { get; set; }
}

public class MenuSection
{
    public required string Header { get; set; }
    public required List<NavItem> NavItems { get; set; }
}

public class NavMenuModel
{
    public required List<MenuSection> MenuSections { get; set; }
}