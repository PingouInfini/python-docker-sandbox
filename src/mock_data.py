import uuid

def generate_mock_messages():
    # Exemple de messages Gazeteer avec UUID fixes
    gazeteer_messages = [
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "ENR": [
                {"type": "Personne", "Valeur": "Adnane", "Position": 7},
                {"type": "Evenement", "Valeur": "Procès", "Position": 18},
                {"type": "Localisation", "Valeur": "Rue de Grenelle", "Position": 42, "MGRS": "4QFJ 12345 67890"}
            ]
        },
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174001",
            "ENR": [
                {"type": "Personne", "Valeur": "Marie", "Position": 4},
                {"type": "Evenement", "Valeur": "Réunion", "Position": 16},
                {"type": "Localisation", "Valeur": "Paris", "Position": 25}
            ]
        },
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174002",
            "ENR": [
                {"type": "Organisation", "Valeur": "Greenpeace", "Position": 9},
                {"type": "Evenement", "Valeur": "Manifestation", "Position": 24},
                {"type": "Localisation", "Valeur": "Place de la République", "Position": 35}
            ]
        },
        # Nouvelles entrées avec des sujets politiques
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174003",
            "ENR": [
                {"type": "Personne", "Valeur": "Emmanuel Macron", "Position": 4},
                {"type": "Evenement", "Valeur": "Discours politique", "Position": 20},
                {"type": "Localisation", "Valeur": "Lyon", "Position": 45}
            ]
        },
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174004",
            "ENR": [
                {"type": "Organisation", "Valeur": "ONU", "Position": 11},
                {"type": "Evenement", "Valeur": "Réunion de l'Assemblée générale", "Position": 28},
                {"type": "Localisation", "Valeur": "New York", "Position": 36}
            ]
        }
    ]

    # Exemple de messages Summarize avec UUID fixes
    summarize_messages = [
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "FilePath": "C:/Documents/Procès_Adnane.pdf",
            "Summary": ("Le procès d'Adnane, qui s'est tenu au tribunal de grande instance de Paris, "
                        "a suscité une attention médiatique considérable. Les témoins ont évoqué les événements "
                        "survenus dans la rue de Grenelle, et les arguments des avocats ont été marqués par des "
                        "interventions passionnées. Le résumé de ce procès, qui a duré plusieurs semaines, met en "
                        "lumière les enjeux sociaux et politiques sous-jacents à cette affaire.")
        },
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174001",
            "FilePath": "C:/Documents/Réunion_Marie.pdf",
            "Summary": ("La réunion à Paris a abordé plusieurs thèmes d'importance stratégique, "
                        "notamment les relations internationales et les négociations politiques. Les intervenants "
                        "ont évoqué l'impact des politiques économiques sur les citoyens et ont proposé des solutions "
                        "pour améliorer la situation économique du pays. Les discussions ont été enrichies par des "
                        "analyses des experts présents.")
        },
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174002",
            "FilePath": "C:/Documents/Greenpeace_Manifestation.pdf",
            "Summary": ("La manifestation organisée par Greenpeace à la Place de la République a été marquée par des "
                        "débats passionnés sur le réchauffement climatique. Des milliers de personnes se sont rassemblées "
                        "pour protester contre les politiques environnementales du gouvernement. Les intervenants ont "
                        "appelé à une prise de conscience collective et ont proposé des actions concrètes pour lutter contre "
                        "la crise climatique mondiale.")
        },
        # Nouvelles entrées avec des sujets politiques
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174003",
            "FilePath": "C:/Documents/Discours_Emmanuel_Macron.pdf",
            "Summary": ("Le discours du président français Emmanuel Macron à Lyon a été marqué par un message fort en faveur "
                        "de l'unité nationale et de la réforme économique. Il a abordé les défis actuels du pays, notamment "
                        "le chômage et la répartition des richesses, tout en soulignant l'importance d'une France forte et "
                        "solidaire sur la scène internationale. Le discours a été bien accueilli par ses partisans, mais "
                        "a suscité des critiques chez certains opposants politiques.")
        },
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174004",
            "FilePath": "C:/Documents/ONU_Réunion.pdf",
            "Summary": ("La réunion de l'Assemblée générale de l'ONU a abordé des sujets cruciaux tels que la sécurité "
                        "internationale, le changement climatique et la migration. Les représentants des nations ont appelé "
                        "à une coopération accrue pour faire face aux défis mondiaux. Des résolutions ont été proposées pour "
                        "renforcer les mécanismes de gouvernance mondiale et protéger les droits humains, tout en cherchant "
                        "des solutions pour réduire les inégalités entre les pays.")
        }
    ]

    return gazeteer_messages, summarize_messages
