def get_update_id(full_variant):
    dict = {
        "Titan_EEA": "https://drive.google.com/uc?id=16zim-aRdfugt_40I18SoDiMSsb2HeLE4",
    }

    return dict[full_variant]


def is_update(full_variant):
    if full_variant == "Titan_UFS":
        return False

    return True
