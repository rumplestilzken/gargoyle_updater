def getOTADictionary():
    dict = {}
    dict["Latest"] = "https://github.com/rumplestilzken/gargoyle_lineageos20/releases/download/ota/ota.json";
    return dict


def get_variant_map(qualifier):
    dict = None
    if "vndk" in qualifier:
        dict = {
            "Titan": "gargoyle_bvN-vndklite",
            "Titan bgn": "gargoyle_pocket_bgn-vndklite",
        }
    elif "bgn" in qualifier:
        dict = {
            "Titan": "gargoyle_bgN",
            "Titan Pocket": "gargoyle_pocket_bgN",
            "Titan Slim": "gargoyle_slim_bgN",
            "Jelly 2E": "gargoyle_jelly2e_bgn",
        }
    else:
        dict = {
            "Titan": "gargoyle_bvN",
            "Titan Pocket": "gargoyle_pocket_bvN",
            "Titan Slim": "gargoyle_slim_bvN",
            "Jelly 2E": "gargoyle_jelly2e_bvn",
        }
    return dict
