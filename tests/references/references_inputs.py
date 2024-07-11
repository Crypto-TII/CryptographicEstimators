REFERENCES_INPUTS = {
    "SDFqEstimator": {
        "gen_sdfq": {
            "gen_sdfq_lee_brickell": {
                "inputs": [(256, 128, 64, 251), (961, 771, 48, 31)]
            },
            "gen_sdfq_stern": {"inputs": [(256, 128, 64, 251), (961, 771, 48, 31)]},
            "gen_sdfq_stern_range": {
                "inputs": [
                    (
                        range(50, 70, 5),
                        range(20, 40, 2),
                        [7, 11, 17, 53, 103, 151, 199, 251],
                    ),
                ]
            },
        },
    },
}
