## Creating a custom spidermon monitor to monitor our scraper

from spidermon import Monitor, MonitorSuite, monitors

@monitors.name("Item count")
class ItemCountMonitor (Monitor):

    @monitors.name("Minimum number of items")
    def test_minimum_number_of_items (self):
        item_extracted = getattr(
            self.data.stats, 'item_scraped_count', 0
        )
        minimum_threshold = 10 # The minimum number of items to be scraped
        msg = 'Extracted less than {} items'.format(minimum_threshold)
        self.assertTrue(
            item_extracted >= minimum_threshold, msg= msg
        )

class SpiderCloseMonitorSuite (MonitorSuite):
    monitors = [ItemCountMonitor, ]
    monitor_finished_actions = [] # Actions to take when suite finishes it's execution
    monitors_failed_actions = [] # Actions to take when a suite finishes it's execution with a failed monitor