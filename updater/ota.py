def getOTADictionary():
    dict = {}
    dict["Latest"] = "https://github.com/rumplestilzken/gargoyle_lineageos20/releases/download/ota/ota.json";
    dict["v1.3"] = "https://github.com/rumplestilzken/gargoyle_lineageos20/releases/download/v1.3/ota.json";
    return dict


def get_variant_map(qualifier):
    dict = None
    if "vndk" in qualifier:
        dict = {
            "Titan": "lineage_gargoyle_bvN-vndklite",
            "Titan bgn": "lineage_gargoyle_pocket_bgN-vndklite",
        }
    elif "bgN" in qualifier:
        dict = {
            "Titan": "lineage_gargoyle_bgN",
            "Titan Pocket": "lineage_gargoyle_pocket_bgN",
            "Titan Slim": "lineage_gargoyle_slim_bgN",
            "Jelly 2E": "lineage_gargoyle_jelly2e_bgN",
        }
    else:
        dict = {
            "Titan": "lineage_gargoyle_bvN",
            "Titan Pocket": "lineage_gargoyle_pocket_bvN",
            "Titan Slim": "lineage_gargoyle_slim_bvN",
            "Jelly 2E": "lineage_gargoyle_jelly2e_bvN",
        }
    return dict

def get_stock_rom_url_by_full_variant(full_variant):
    dict = {
        "Titan_EEA": "https://drive.google.com/uc?id=1oCChPMHQYWhOId4u2lZCJuP3VIJ87glR",
        "Titan_TEE": "https://drive.google.com/uc?id=1Nc5WdJt1K6DVUiq4EGo7RrMM_ukKvh6M",
        "Titan_UFS": "https://drive.google.com/uc?id=1UtPFygiYztL_aHKw13Pb4aKiLDmLAm1I",
        "Pocket_EEA": "https://drive.google.com/uc?id=1bL0QO-rmMTnsEtEXYm6aetdXd-y8I19g",
        "Pocket_TEE": "https://drive.google.com/uc?id=1HZZ84TOGcj6zQcGn5_o1i0CW5GfI6H4D",
        #TODO: Slim and Jelly 2E
    }
    return dict[full_variant]
