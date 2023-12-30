import unittest

import trussme


class TestCustomStuff(unittest.TestCase):
    def test_custom_material(self):
        # Build truss from scratch
        truss = trussme.Truss()
        truss.add_pinned_joint([0.0, 0.0, 0.0])
        truss.add_free_joint([2.5, 2.5, 0.0])
        truss.add_roller_joint([5.0, 0.0, 0.0])

        truss.add_out_of_plane_support("z")

        truss.joints[1].loads[1] = -20000

        unobtanium: trussme.Material = {
            "name": "unobtanium",
            "yield_strength": 200_000_000_000,
            "elastic_modulus": 200_000_000_000_000.0,
            "density": 1_000.0,
        }

        truss.add_member(0, 1, material=unobtanium)
        truss.add_member(1, 2, material=unobtanium)
        truss.add_member(2, 0, material=unobtanium)

        goals = trussme.Goals(
            minimum_fos_buckling=1.5,
            minimum_fos_yielding=1.5,
            maximum_mass=5.0,
            maximum_deflection=6e-3,
        )

        print(truss.report(goals))

    def test_custom_shape(self):
        # Build truss from scratch
        truss = trussme.Truss()
        truss.add_pinned_joint([0.0, 0.0, 0.0])
        truss.add_free_joint([2.5, 2.5, 0.0])
        truss.add_roller_joint([5.0, 0.0, 0.0])

        truss.add_out_of_plane_support("z")

        truss.joints[1].loads[1] = -20000

        class MagicalRod(trussme.Shape):
            def __init__(self):
                self.h = None
                self.w = None
                self.r = None
                self.t = None

            def moi(self) -> float:
                return 200_000_000_000

            def area(self) -> float:
                return 200_000_000_000

            def name(self) -> str:
                return "magical rod"

        truss.add_member(0, 1, shape=MagicalRod())
        truss.add_member(1, 2, shape=MagicalRod())
        truss.add_member(2, 0, shape=MagicalRod())

        goals = trussme.Goals(
            minimum_fos_buckling=1.5,
            minimum_fos_yielding=1.5,
            maximum_mass=5.0,
            maximum_deflection=6e-3,
        )

        print(truss.report(goals))
