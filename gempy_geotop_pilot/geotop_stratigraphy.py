import gempy as gp

"""
HL
BX KR BE KW WB EE KROE DR DT DN URTY PE UR ST AP SY PZWA
MS 
KI
OO
IE BR
VE RU TO DO LA HT HO MT GU VA AK

"""

stratigraphy_pile = {
    "1"  : "HL",
    "1.5": ("BX"),  # * BX - BE there is unconformity
    "1.6": ("KR", "BE", "KW", "WB", "EE", "KROE"),
    "2"  : ("DR", "DT", "DN", "URTY", "PE", "UR", "ST", "AP"),  # * ST, SY, PXWA - Are Conformable
    "2.3": ("SY"),
    "2.6": ("PZWA"),
    "3"  : "MS",  # * MS - KI there is unconformity
    "4"  : ("KI"),  # * KI - OO are comformable
    "5"  : ("OO"),
    "6"  : ("IE", "BR"),
    "7"  : ("VE", "RU", "TO", "DO", "LA", "HT", "HO", "MT", "GU", "VA", "AK")  # * I have no idea about these
}
elements_colors = {
    "HL"  : "#0c810c",
    "BX"  : "#ffeb00",
    "KR"  : "#af2d5e",
    "BE"  : "#c8c8ff",
    "KW"  : "#aca92b",
    "WB"  : "#89431e",
    "EE"  : "#89431e",
    "KROE": "#ba3f79",
    "DR"  : "#ff7f50",
    "DT"  : "#9d9d9d",
    "DN"  : "#fafad2",
    "URTY": "#a9a357",
    "PE"  : "#ee82ee",
    "UR"  : "#bdb76b",
    "ST"  : "#cd5c5c",
    "AP"  : "#daa520",
    "SY"  : "#ffe4b5",
    "PZWA": "#ffcc00",
    "MS"  : "#87ceeb",
    "KI"  : "#bc8f8f",
    "OO"  : "#769d27",
    "IE"  : "#ec79c1",
    "BR"  : "#6cbc96",
    "VE"  : "#666410",
    "RU"  : "#b87bee",
    "TO"  : "#5a9fdb",
    "DO"  : "#d8bfd8",
    "LA"  : "#d02090",
    "HT"  : "#b42828",
    "HO"  : "#d2691e",
    "MT"  : "#ffa066",
    "GU"  : "#f5deb3",
    "VA"  : "#15994f",
    "AK"  : "#98e7cd"
}


def color_elements(elements: list[gp.data.StructuralElement]):
    for element in elements:
        name_ = elements_colors.get(element.name, "#000000")  # ? I think this is black. Not good for basement
        element.color = name_
