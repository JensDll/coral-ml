import pathlib
from modules import core


class TestLoadLabels:
    def test_basic(self):
        path = pathlib.Path(f"{__file__}/../assets/basic.txt")
        labels = core.coral.load_labels(path)
        assert labels == {
            0: "background",
            1: "tench, Tinca tinca",
            2: "goldfish, Carassius auratus",
            3: "tiger shark, Galeocerdo cuvieri",
        }

    def test_csv(self):
        path = pathlib.Path(f"{__file__}/../assets/csv.txt")
        labels = core.coral.load_labels(path)
        assert labels == {
            0: "Tortillaland Flour Small Fresh Uncooked Tortillas - 11.52 oz",
            1: "Hostess Coffee, Twinkies, Cups - 12 pack, 0.33 oz cups",
            2: "Pics Mozzarella Cheese Sticks - 8 oz",
            3: "Refreshe Drink Mix, Sugar Free, Fruit Punch - 6 pack, 0.34 oz packets",
        }
