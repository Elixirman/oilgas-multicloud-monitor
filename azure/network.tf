resource "azurerm_resource_group" "field_rg" {
  name     = "field-rg"
  location = "East US"
}

resource "azurerm_virtual_network" "field_vnet" {
  name                = "field-vnet"
  address_space       = ["10.1.0.0/16"]
  location            = azurerm_resource_group.field_rg.location
  resource_group_name = azurerm_resource_group.field_rg.name
}

resource "azurerm_subnet" "field_subnet" {
  name                 = "field-subnet"
  resource_group_name  = azurerm_resource_group.field_rg.name
  virtual_network_name = azurerm_virtual_network.field_vnet.name
  address_prefixes     = ["10.1.1.0/24"]
}

resource "azurerm_subnet" "gateway_subnet" {
  name                 = "GatewaySubnet"
  resource_group_name  = azurerm_resource_group.field_rg.name
  virtual_network_name = azurerm_virtual_network.field_vnet.name
  address_prefixes     = ["10.1.2.0/27"]
}

resource "azurerm_network_security_group" "field_nsg" {
  name                = "field-nsg"
  location            = azurerm_resource_group.field_rg.location
  resource_group_name = azurerm_resource_group.field_rg.name

  security_rule {
    name                       = "Allow-SSH-Admin"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "102.88.106.32/32"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "Allow-Outbound-AWS"
    priority                   = 110
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "10.0.0.0/16"
  }
}

resource "azurerm_subnet_network_security_group_association" "field_nsg_assoc" {
  subnet_id                 = azurerm_subnet.field_subnet.id
  network_security_group_id = azurerm_network_security_group.field_nsg.id
}
