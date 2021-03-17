import bpy
from .constants import firstNodeId
from .defaultKey import defaultKey

def add_code_relay_logo(game):
    # type: (bpy.SceneTreeOutputType) -> bpy.SceneTreeOutputType
    """Adds the code relay logo.io to the beginning of the font game.
  Don't be a jerk. Leave the logo intact. I've made the entire software 
  free as in freedom, all I ask is that my logo stays in the front, so I 
  can attract more people to work on open source software to make the 
  world a better place."""
    logo_frames = [{
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2387
            }, {
                "x": -18,
                "y": 374
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2153
            }, {
                "x": -18,
                "y": 142
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo50000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0022.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0023.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "Contribute": [{
                "x": -16,
                "y": -889
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo30000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0024.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "Contribute": [{
                "x": -16,
                "y": -889
            }],
            "to": [{
                "x": 1084,
                "y": -889
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0025.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "Contribute": [{
                "x": -16,
                "y": -889
            }],
            "to": [{
                "x": 1084,
                "y": -889
            }],
            "open": [{
                "x": 1384,
                "y": -889
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo50000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0026.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "Contribute": [{
                "x": -16,
                "y": -889
            }],
            "to": [{
                "x": 1084,
                "y": -889
            }],
            "open": [{
                "x": 1384,
                "y": -889
            }],
            "source": [{
                "x": 1884,
                "y": -889
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0027.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "Contribute": [{
                "x": -16,
                "y": -889
            }],
            "to": [{
                "x": 1084,
                "y": -889
            }],
            "open": [{
                "x": 1384,
                "y": -889
            }],
            "source": [{
                "x": 1884,
                "y": -889
            }],
            "in": [{
                "x": -16,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo30000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0028.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "Contribute": [{
                "x": -16,
                "y": -889
            }],
            "to": [{
                "x": 1084,
                "y": -889
            }],
            "open": [{
                "x": 1384,
                "y": -889
            }],
            "source": [{
                "x": 1884,
                "y": -889
            }],
            "in": [{
                "x": -16,
                "y": -1059
            }],
            "15": [{
                "x": 284,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0029.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "Contribute": [{
                "x": -16,
                "y": -889
            }],
            "to": [{
                "x": 1084,
                "y": -889
            }],
            "open": [{
                "x": 1384,
                "y": -889
            }],
            "source": [{
                "x": 1884,
                "y": -889
            }],
            "in": [{
                "x": -16,
                "y": -1059
            }],
            "15": [{
                "x": 284,
                "y": -1059
            }],
            "min.": [{
                "x": 584,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo50000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0030.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "Contribute": [{
                "x": -16,
                "y": -889
            }],
            "to": [{
                "x": 1084,
                "y": -889
            }],
            "open": [{
                "x": 1384,
                "y": -889
            }],
            "source": [{
                "x": 1884,
                "y": -889
            }],
            "in": [{
                "x": -16,
                "y": -1059
            }],
            "15": [{
                "x": 284,
                "y": -1059
            }],
            "min.": [{
                "x": 584,
                "y": -1059
            }],
            "Then,": [{
                "x": 1084,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0031.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "Contribute": [{
                "x": -16,
                "y": -889
            }],
            "to": [{
                "x": 1084,
                "y": -889
            }],
            "open": [{
                "x": 1384,
                "y": -889
            }],
            "source": [{
                "x": 1884,
                "y": -889
            }],
            "in": [{
                "x": -16,
                "y": -1059
            }],
            "15": [{
                "x": 284,
                "y": -1059
            }],
            "min.": [{
                "x": 584,
                "y": -1059
            }],
            "Then,": [{
                "x": 1084,
                "y": -1059
            }],
            "pass": [{
                "x": 1684,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo30000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0032.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "Contribute": [{
                "x": -16,
                "y": -889
            }],
            "to": [{
                "x": 1084,
                "y": -889
            }],
            "open": [{
                "x": 1384,
                "y": -889
            }],
            "source": [{
                "x": 1884,
                "y": -889
            }],
            "in": [{
                "x": -16,
                "y": -1059
            }],
            "15": [{
                "x": 284,
                "y": -1059
            }],
            "min.": [{
                "x": 584,
                "y": -1059
            }],
            "Then,": [{
                "x": 1084,
                "y": -1059
            }],
            "pass": [{
                "x": 1684,
                "y": -1059
            }],
            "it": [{
                "x": 2184,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0033.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "in": [{
                "x": -16,
                "y": -889
            }],
            "15": [{
                "x": 284,
                "y": -889
            }],
            "min.": [{
                "x": 584,
                "y": -889
            }],
            "Then,": [{
                "x": 1084,
                "y": -889
            }],
            "pass": [{
                "x": 1684,
                "y": -889
            }],
            "it": [{
                "x": 2184,
                "y": -889
            }, {
                "x": -16,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo50000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0034.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "in": [{
                "x": -16,
                "y": -889
            }],
            "15": [{
                "x": 284,
                "y": -889
            }],
            "min.": [{
                "x": 584,
                "y": -889
            }],
            "Then,": [{
                "x": 1084,
                "y": -889
            }],
            "pass": [{
                "x": 1684,
                "y": -889
            }],
            "it": [{
                "x": 2184,
                "y": -889
            }, {
                "x": -16,
                "y": -1059
            }],
            "on": [{
                "x": 284,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0035.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "in": [{
                "x": -16,
                "y": -889
            }],
            "15": [{
                "x": 284,
                "y": -889
            }],
            "min.": [{
                "x": 584,
                "y": -889
            }],
            "Then,": [{
                "x": 1084,
                "y": -889
            }],
            "pass": [{
                "x": 1684,
                "y": -889
            }],
            "it": [{
                "x": 2184,
                "y": -889
            }, {
                "x": -16,
                "y": -1059
            }],
            "on": [{
                "x": 284,
                "y": -1059
            }],
            "to": [{
                "x": 584,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo30000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0022.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "in": [{
                "x": -16,
                "y": -889
            }],
            "15": [{
                "x": 284,
                "y": -889
            }],
            "min.": [{
                "x": 584,
                "y": -889
            }],
            "Then,": [{
                "x": 1084,
                "y": -889
            }],
            "pass": [{
                "x": 1684,
                "y": -889
            }],
            "it": [{
                "x": 2184,
                "y": -889
            }, {
                "x": -16,
                "y": -1059
            }],
            "on": [{
                "x": 284,
                "y": -1059
            }],
            "to": [{
                "x": 584,
                "y": -1059
            }],
            "the": [{
                "x": 884,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0023.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "in": [{
                "x": -16,
                "y": -889
            }],
            "15": [{
                "x": 284,
                "y": -889
            }],
            "min.": [{
                "x": 584,
                "y": -889
            }],
            "Then,": [{
                "x": 1084,
                "y": -889
            }],
            "pass": [{
                "x": 1684,
                "y": -889
            }],
            "it": [{
                "x": 2184,
                "y": -889
            }, {
                "x": -16,
                "y": -1059
            }],
            "on": [{
                "x": 284,
                "y": -1059
            }],
            "to": [{
                "x": 584,
                "y": -1059
            }],
            "the": [{
                "x": 884,
                "y": -1059
            }],
            "next": [{
                "x": 1284,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo50000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0024.coderelay.png": [{
                "x": 285,
                "y": -1242
            }]
        },
        "words": {
            "it": [{
                "x": -16,
                "y": -889
            }],
            "on": [{
                "x": 284,
                "y": -889
            }],
            "to": [{
                "x": 584,
                "y": -889
            }],
            "the": [{
                "x": 884,
                "y": -889
            }],
            "next": [{
                "x": 1284,
                "y": -889
            }],
            "contributor.": [{
                "x": -16,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "Run0025.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -1059
            }]
        },
        "words": {
            "contributor.": [{
                "x": -16,
                "y": -889
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "Run0026.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "codeRelayLogo30000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -1059
            }]
        },
        "words": {
            "contributor.": [{
                "x": -16,
                "y": -889
            }],
            "relay": [{
                "x": 184,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "Run0027.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -1059
            }]
        },
        "words": {
            "contributor.": [{
                "x": -16,
                "y": -889
            }],
            "relay": [{
                "x": 184,
                "y": -1059
            }],
            "race": [{
                "x": 784,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "Run0028.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "codeRelayLogo50000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -1059
            }]
        },
        "words": {
            "contributor.": [{
                "x": -16,
                "y": -889
            }],
            "relay": [{
                "x": 184,
                "y": -1059
            }],
            "race": [{
                "x": 784,
                "y": -1059
            }],
            "for": [{
                "x": 1284,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "Run0029.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -1059
            }]
        },
        "words": {
            "contributor.": [{
                "x": -16,
                "y": -889
            }],
            "relay": [{
                "x": 184,
                "y": -1059
            }],
            "race": [{
                "x": 784,
                "y": -1059
            }],
            "for": [{
                "x": 1284,
                "y": -1059
            }],
            "code!": [{
                "x": 1684,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "Run0030.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "codeRelayLogo30000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -889
            }]
        },
        "words": {
            "relay": [{
                "x": 184,
                "y": -889
            }],
            "race": [{
                "x": 784,
                "y": -889
            }],
            "for": [{
                "x": 1284,
                "y": -889
            }],
            "code!": [{
                "x": 1684,
                "y": -889
            }],
            "CodeRelay.io!": [{
                "x": -16,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "Run0031.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "capitalP.png": [{
                "x": 1261,
                "y": -1227
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -889
            }]
        },
        "words": {
            "relay": [{
                "x": 184,
                "y": -889
            }],
            "race": [{
                "x": 784,
                "y": -889
            }],
            "for": [{
                "x": 1284,
                "y": -889
            }],
            "code!": [{
                "x": 1684,
                "y": -889
            }],
            "CodeRelay.io!": [{
                "x": -16,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "Run0032.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "capitalP.png": [{
                "x": 1261,
                "y": -1227
            }],
            "capitalR.png": [{
                "x": 1361,
                "y": -1227
            }],
            "codeRelayLogo50000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -889
            }]
        },
        "words": {
            "relay": [{
                "x": 184,
                "y": -889
            }],
            "race": [{
                "x": 784,
                "y": -889
            }],
            "for": [{
                "x": 1284,
                "y": -889
            }],
            "code!": [{
                "x": 1684,
                "y": -889
            }],
            "CodeRelay.io!": [{
                "x": -16,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "Run0033.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "capitalP.png": [{
                "x": 1261,
                "y": -1227
            }],
            "capitalR.png": [{
                "x": 1361,
                "y": -1227
            }],
            "capitalE.png": [{
                "x": 1461,
                "y": -1227
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -889
            }]
        },
        "words": {
            "relay": [{
                "x": 184,
                "y": -889
            }],
            "race": [{
                "x": 784,
                "y": -889
            }],
            "for": [{
                "x": 1284,
                "y": -889
            }],
            "code!": [{
                "x": 1684,
                "y": -889
            }],
            "CodeRelay.io!": [{
                "x": -16,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "capitalP.png": [{
                "x": 1261,
                "y": -1227
            }],
            "capitalR.png": [{
                "x": 1361,
                "y": -1227
            }],
            "capitalE.png": [{
                "x": 1461,
                "y": -1227
            }],
            "capitalS.png": [{
                "x": 1561,
                "y": -1227
            }],
            "Run0034.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "codeRelayLogo30000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -889
            }]
        },
        "words": {
            "relay": [{
                "x": 184,
                "y": -889
            }],
            "race": [{
                "x": 784,
                "y": -889
            }],
            "for": [{
                "x": 1284,
                "y": -889
            }],
            "code!": [{
                "x": 1684,
                "y": -889
            }],
            "CodeRelay.io!": [{
                "x": -16,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "capitalP.png": [{
                "x": 1261,
                "y": -1227
            }],
            "capitalR.png": [{
                "x": 1361,
                "y": -1227
            }],
            "capitalE.png": [{
                "x": 1461,
                "y": -1227
            }, {
                "x": 1661,
                "y": -1227
            }],
            "capitalS.png": [{
                "x": 1561,
                "y": -1227
            }],
            "Run0035.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -889
            }]
        },
        "words": {
            "relay": [{
                "x": 184,
                "y": -889
            }],
            "race": [{
                "x": 784,
                "y": -889
            }],
            "for": [{
                "x": 1284,
                "y": -889
            }],
            "code!": [{
                "x": 1684,
                "y": -889
            }],
            "CodeRelay.io!": [{
                "x": -16,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "capitalP.png": [{
                "x": 1261,
                "y": -1227
            }],
            "capitalR.png": [{
                "x": 1361,
                "y": -1227
            }],
            "capitalE.png": [{
                "x": 1461,
                "y": -1227
            }, {
                "x": 1661,
                "y": -1227
            }],
            "capitalS.png": [{
                "x": 1561,
                "y": -1227
            }],
            "capitalN.png": [{
                "x": 1761,
                "y": -1227
            }],
            "Run0022.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "codeRelayLogo50000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -889
            }]
        },
        "words": {
            "relay": [{
                "x": 184,
                "y": -889
            }],
            "race": [{
                "x": 784,
                "y": -889
            }],
            "for": [{
                "x": 1284,
                "y": -889
            }],
            "code!": [{
                "x": 1684,
                "y": -889
            }],
            "CodeRelay.io!": [{
                "x": -16,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "capitalP.png": [{
                "x": 1261,
                "y": -1227
            }],
            "capitalR.png": [{
                "x": 1361,
                "y": -1227
            }],
            "capitalE.png": [{
                "x": 1461,
                "y": -1227
            }, {
                "x": 1661,
                "y": -1227
            }],
            "capitalS.png": [{
                "x": 1561,
                "y": -1227
            }],
            "capitalN.png": [{
                "x": 1761,
                "y": -1227
            }],
            "capitalT.png": [{
                "x": 1861,
                "y": -1227
            }],
            "Run0023.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -889
            }]
        },
        "words": {
            "relay": [{
                "x": 184,
                "y": -889
            }],
            "race": [{
                "x": 784,
                "y": -889
            }],
            "for": [{
                "x": 1284,
                "y": -889
            }],
            "code!": [{
                "x": 1684,
                "y": -889
            }],
            "CodeRelay.io!": [{
                "x": -16,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "capitalP.png": [{
                "x": 1261,
                "y": -1227
            }],
            "capitalR.png": [{
                "x": 1361,
                "y": -1227
            }],
            "capitalE.png": [{
                "x": 1461,
                "y": -1227
            }, {
                "x": 1661,
                "y": -1227
            }],
            "capitalS.png": [{
                "x": 1561,
                "y": -1227
            }, {
                "x": 1961,
                "y": -1227
            }],
            "capitalN.png": [{
                "x": 1761,
                "y": -1227
            }],
            "capitalT.png": [{
                "x": 1861,
                "y": -1227
            }],
            "Run0024.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "codeRelayLogo30000.coderelay.png": [{
                "x": -46,
                "y": -438
            }],
            "capitalA.png": [{
                "x": -16,
                "y": -889
            }]
        },
        "words": {
            "relay": [{
                "x": 184,
                "y": -889
            }],
            "race": [{
                "x": 784,
                "y": -889
            }],
            "for": [{
                "x": 1284,
                "y": -889
            }],
            "code!": [{
                "x": 1684,
                "y": -889
            }],
            "CodeRelay.io!": [{
                "x": -16,
                "y": -1059
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "capitalP.png": [{
                "x": 1261,
                "y": -1227
            }],
            "capitalR.png": [{
                "x": 1361,
                "y": -1227
            }],
            "capitalE.png": [{
                "x": 1461,
                "y": -1227
            }, {
                "x": 1661,
                "y": -1227
            }],
            "capitalS.png": [{
                "x": 1561,
                "y": -1227
            }, {
                "x": 1961,
                "y": -1227
            }],
            "capitalN.png": [{
                "x": 1761,
                "y": -1227
            }],
            "capitalT.png": [{
                "x": 1861,
                "y": -1227
            }],
            "period.png": [{
                "x": 2061,
                "y": -1227
            }],
            "Run0025.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "codeRelayLogo40000.coderelay.png": [{
                "x": -46,
                "y": -438
            }]
        }
    }, {
        "sprites": {
            "blackBar.coderelay.png": [{
                "x": -18,
                "y": -2026
            }, {
                "x": -18,
                "y": 17
            }],
            "capitalP.png": [{
                "x": 1261,
                "y": -1227
            }],
            "capitalR.png": [{
                "x": 1361,
                "y": -1227
            }],
            "capitalE.png": [{
                "x": 1461,
                "y": -1227
            }, {
                "x": 1661,
                "y": -1227
            }],
            "capitalS.png": [{
                "x": 1561,
                "y": -1227
            }, {
                "x": 1961,
                "y": -1227
            }],
            "capitalN.png": [{
                "x": 1761,
                "y": -1227
            }],
            "capitalT.png": [{
                "x": 1861,
                "y": -1227
            }],
            "period.png": [{
                "x": 2061,
                "y": -1227
            }, {
                "x": 2161,
                "y": -1227
            }],
            "Run0026.coderelay.png": [{
                "x": 285,
                "y": -1242
            }],
            "codeRelayLogo50000.coderelay.png": [{
                "x": -46,
                "y": -438
            }]
        }
    }]  # type: (list[bpy.FrameInfo])

    num = 0
    while f"actual_first_node{num}" in game['nodes']:
        num += 1
    new_node_id = f"actual_first_node{num}"

    scene_num = 0
    while f"scene_scene_scene{scene_num}" in game['scenes']:
        scene_num += 1
    synthetic_scene_name = f"scene_scene_scene{scene_num}"

    first_node = game["nodes"][firstNodeId]

    game["nodes"][new_node_id] = first_node

    synthetic_first_node = {
        'conditions': [{
            'key': defaultKey,
            'node_id': new_node_id
        }],
        'scene_name': synthetic_scene_name,
        'slots': []
    }  # type: bpy.SceneNodeInfoType
    game['nodes'][firstNodeId] = synthetic_first_node
    synthetic_scene = {
        'frames': logo_frames,
        'slots': 0
    }  # type: bpy.SceneInfoType
    game['scenes'][synthetic_scene_name] = synthetic_scene
    return game
