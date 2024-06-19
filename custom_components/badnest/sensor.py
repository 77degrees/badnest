import logging

from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.entity import Entity
import homeassistant.util.temperature as temperature_util

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Nest sensors."""
    api = hass.data[DOMAIN]['api']

    sensors = []
    _LOGGER.info("Adding sensors")
    for sensor in api['sensors']:
        _LOGGER.info(f"Adding nest sensor uuid: {sensor}")
        sensors.append(NestSensor(sensor, api))

    async_add_entities(sensors)

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return temperature_util.celsius_to_fahrenheit(celsius)

class NestSensor(Entity):
    """Representation of a Nest sensor."""

    def __init__(self, device_id, api):
        """Initialize the sensor."""
        self.device_id = device_id
        self.device = api
        self._unit_of_measurement = UnitOfTemperature.FAHRENHEIT

    @property
    def unique_id(self):
        """Return an unique ID."""
        return self.device_id

    @property
    def name(self):
        """Return a friendly name."""
        return self.device.device_data[self.device_id]['name']

    @property
    def state(self):
        """Return the state of the sensor."""
        temp_celsius = self.device.device_data[self.device_id]['current_temperature']
        if self._unit_of_measurement == UnitOfTemperature.FAHRENHEIT:
            return celsius_to_fahrenheit(temp_celsius)
        return temp_celsius

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def device_class(self):
        """Return the device class."""
        return "temperature"

    def update(self):
        """Fetch new state data for the sensor."""
        self.device.update()
