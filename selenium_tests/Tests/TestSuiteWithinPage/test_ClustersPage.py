import pytest

from selenium_tests.Pages.ClustersPage import ClustersPage


@pytest.mark.usefixtures("tear_up_down")
class Test_ClustersPage:

    def test_crucial_elements_visibility(self):
        page = ClustersPage(self.driver)
        assert page.get_number_of_clusters() > 0

