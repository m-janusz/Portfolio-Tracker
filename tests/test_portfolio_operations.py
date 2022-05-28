import unittest

from pathlib import Path
from typing import Dict

from src.controllers.portfolio_controller import PortfolioController


class TestAddAsset(unittest.TestCase):
    def setUp(self) -> None:
        self.portfolio_controller = PortfolioController(Path("/"), "test")

        self._asset_template = {
            "name": "Test",
            "unit_price": 1,
            "amount": 10,
            "currency": "USD",
        }

        return super().setUp()

    @property
    def asset_template(self) -> Dict:
        return self._asset_template.copy()

    def _check_add_valid_asset(self, test_asset: Dict) -> None:
        """Add asset to portfolio and check if it is in portfolio assets
        and has the same values as provided in arguments.
        """

        self.portfolio_controller.add_asset(
            test_asset["name"],
            test_asset["unit_price"],
            test_asset["amount"],
            test_asset["currency"],
        )

        assets = self.portfolio_controller._portfolio._assets

        # test if test asset name in assets
        self.assertIn(test_asset["name"], assets.keys())

        asset = assets[test_asset["name"]]

        # test if the values are the same
        self.assertEqual(asset["unit_price"], test_asset["unit_price"])
        self.assertEqual(asset["amount"], test_asset["amount"])
        self.assertEqual(asset["currency"], test_asset["currency"])

    def _check_add_asset_exception(
        self, test_asset: Dict, exception: Exception
    ) -> None:
        """Check if portoflio add_asset raises provided exception,
        also check if asset is not added into portfolio assets.
        """

        self.assertRaises(
            exception,
            self.portfolio_controller.add_asset,
            test_asset["name"],
            test_asset["unit_price"],
            test_asset["amount"],
            test_asset["currency"],
        )

        assets = self.portfolio_controller._portfolio._assets

        # check if asset was not added to assets
        self.assertNotIn(test_asset["name"], assets.keys())

    def test_add_example(self) -> None:
        """Test portfolio controller add_asset function
        provided valid example arguments

        Should add an asset to portfolio with values provided in arguments.
        """

        test_asset = self.asset_template
        self._check_add_valid_asset(test_asset)

    def test_add_empty_name(self) -> None:
        """Test portfolio controller add_asset function
        provided with empty string as name argument

        Should raise ValueError
        """

        test_asset = self.asset_template
        test_asset["name"] = ""

        self._check_add_asset_exception(test_asset, ValueError)

    def test_add_negative_unitprice(self) -> None:
        """Test portfolio controller add_asset function
        provided with empty string as unit price argument

        Should raise ValueError
        """

        test_asset = self.asset_template
        test_asset["unit_price"] = -1

        self._check_add_asset_exception(test_asset, ValueError)

    def test_add_negative_amount(self) -> None:
        """Test portfolio controller add_asset function
        provided with empty string as amount argument

        Should raise ValueError
        """

        test_asset = self.asset_template
        test_asset["amount"] = -10
        self._check_add_asset_exception(test_asset, ValueError)

    def test_add_empty_currency(self) -> None:
        """Test portfolio controller add_asset function
        provided with empty string as currency argument

        Should raise ValueError
        """

        test_asset = self.asset_template
        test_asset["currency"] = ""
        self._check_add_asset_exception(test_asset, ValueError)


class TestRemoveAsset(unittest.TestCase):
    def setUp(self) -> None:
        self.portfolio_controller = PortfolioController(Path("/"), "test")

        # constants for test asset
        self._TEST_ASSET_NAME = "testname"
        self._TEST_ASSET_UNIT_PRICE = 100
        self._TEST_ASSET_AMOUNT = 1000
        self._TEST_ASSET_CURRENCY = "USD"

        # create test asset inside portfolio
        self._initialize_example_portfolio()

        return super().setUp()

    def _initialize_example_portfolio(self) -> None:
        """Create portfolio with example asset"""

        self.portfolio_controller._portfolio.assets[self._TEST_ASSET_NAME] = {
            "unit_price": self._TEST_ASSET_UNIT_PRICE,
            "amount": self._TEST_ASSET_AMOUNT,
            "currency": self._TEST_ASSET_CURRENCY,
        }

    def _check_remove_asset_exception(self, name, amount, exception) -> None:
        """Call remove_asset with provided arguments
        and check if provided exception was raised
        """

        self.assertRaises(
            exception, self.portfolio_controller.remove_asset, name, amount
        )

    def _check_remove_asset_valid(self, name, amount) -> None:
        """Remove asset with provided arguments

        If removed amount is less than current amount of asset
        check if amount after removal is correct

        else check if asset was removed from the portfolio
        """

        self.portfolio_controller.remove_asset(name, amount)
        if amount < self._TEST_ASSET_AMOUNT:
            self.assertEqual(
                self.portfolio_controller._portfolio.assets[name]["amount"],
                self._TEST_ASSET_AMOUNT - amount,
            )
        else:
            self.assertNotIn(name, self.portfolio_controller._portfolio.assets)

    def test_remove_nonexisting_asset(self) -> None:
        """Test removing asset without name from portfolio.

        Should raise ValueError
        """

        self._check_remove_asset_exception("", 10, ValueError)
        self._initialize_example_portfolio()

    def test_remove_negative_amount(self) -> None:
        """Test negative amount of assets from portfolio.

        Should raise ValueError
        """

        self._check_remove_asset_exception("testname", -10, ValueError)
        self._initialize_example_portfolio()

    def test_remove_not_all_assets(self) -> None:
        """Test removing amount of asset less than current amount

        Should decrease amount of asset"""

        self._check_remove_asset_valid("testname", self._TEST_ASSET_AMOUNT - 1)
        self._initialize_example_portfolio()

    def test_remove_all_assets(self) -> None:
        """Test removing whole amount of asset

        Should remove asset from portfolio"""

        self._check_remove_asset_valid("testname", self._TEST_ASSET_AMOUNT)
        self._initialize_example_portfolio()


if __name__ == "__main__":
    unittest.main()
