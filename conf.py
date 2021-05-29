from configparser import ConfigParser
config = ConfigParser()

config.read('config.ini')
config.add_section('main')
config.set('main', 'number_of_ISPs', '4')
config.set('main', 'number_of_SIs', '10')
config.set('main', 'number_of_consumers', '400')
config.set('main', 'number_of_steps', '20')
config.set('main', 'market_share', '2, 4, 3, 1')
config.set('main', 'investment_URLLC', '80')
config.set('main', 'investment_mMTC', '20')
config.set('main', 'URLLC_spectrum_capacity', '10')
config.set('main', 'mMTC_spectrum_capacity', '20')
config.set('main', 'URLLC_infrastructure_cost', '80')
config.set('main', 'mMTC_infrastructure_cost', '20')
config.set('main', 'agent_year_update', '50, 75, 150, 75, 50')
# market_share=[2, 4, 3, 1]
# investment_URLLC=80, investment_mMTC=20, URLLC_spectrum_capacity=10,
#  mMTC_spectrum_capacity=20, URLLC_infrastructure_cost=80, mMTC_infrastructure_cost=20

with open('config.ini', 'w') as f:
    config.write(f)

