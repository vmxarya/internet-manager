from core.decision import DecisionEngine


engine = DecisionEngine(
    "TCI",
    "Irancell"
)


tests = [

    {
        "TCI":100,
        "Irancell":100
    },


    {
        "TCI":40,
        "Irancell":90
    },


    {
        "TCI":90,
        "Irancell":80
    }

]


for t in tests:

    print("\nScores:")
    print(t)

    result = engine.decide(t)

    print("Active:", result)
