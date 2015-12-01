import datetime
from eventsourcing.domain.model.events import publish
from mock import patch
from mock import MagicMock
from twisted.trial import unittest

from quantdsl.domain.model.market_calibration import MarketCalibrationRepository, MarketCalibration
from quantdsl.domain.model.market_simulation import MarketSimulation, MarketSimulationRepository
from quantdsl.infrastructure.simulation_subscriber import SimulationSubscriber


class TestSimulationSubscriber(unittest.TestCase):

    def setUp(self):
        market_simulation_repo = MagicMock(spec=MarketSimulationRepository)
        market_calibration_repo = MagicMock(spec=MarketCalibrationRepository)

        self.simulation_subscriber = SimulationSubscriber(market_calibration_repo, market_simulation_repo)

    def tearDown(self):
        self.simulation_subscriber.close()

    @patch('quantdsl.infrastructure.simulation_subscriber.generate_simulated_prices')
    def test_simulation_subscriber(self, generate_simulated_prices):
        # Check that when an event is published, the domain service is called.
        market_simulation_created = MarketSimulation.Created(
            entity_id='1',
            market_calibration_id='1',
            market_names=[],
            fixing_dates=[],
            observation_date=datetime.date(2011, 1, 1,),
            path_count=2,
            interest_rate=2.5,
        )
        self.assertEqual(generate_simulated_prices.call_count, 0)
        publish(market_simulation_created)
        self.assertEqual(generate_simulated_prices.call_count, 1)