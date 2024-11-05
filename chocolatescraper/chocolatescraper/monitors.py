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


@monitors.name('Item validation')
class ItemValidationMonitor (Monitor):
    @monitors.name('No item vavlidation errors')
    def test_no_item_vavlidation_errors (self):
        validation_errors = getattr(
            'self.stats',
            'spidermon/validation/fields/errors',
            0
        )
        self.assertEqual(
            validation_errors,
            0,
            msg = 'Found validation errors in fields {}'.format(validation_errors)
        )


class SpiderCloseMonitorSuite (MonitorSuite):
    monitors = [ItemCountMonitor, ItemValidationMonitor]
    monitor_finished_actions = [] # Actions to take when suite finishes it's execution
    monitors_failed_actions = [] # Actions to take when a suite finishes it's execution with a failed monitor

# Definning a periodic montior
class PeriodicMonitorSuite (MonitorSuite):
    monitors = [ItemValidationMonitor,  ]