import random
from agents import City, ISP, SystemIntegrator, Consumer
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

conf = config['main']
number_of_ISPs=int(conf["number_of_ISPs"])
number_of_SIs=int(conf["number_of_SIs"])
number_of_consumers=int(conf["number_of_consumers"])
number_of_steps=int(conf["number_of_steps"])
market_share_string=conf.get("market_share")
market_share=list(map(int, market_share_string.split(',')))
agent_year_update_string=conf.get("agent_year_update")
agent_year_update=list(map(int, agent_year_update_string.split(',')))
# print(market_share)


list_of_ISPs = []
list_of_SIs = []
list_of_consumers = []

for k in range(number_of_consumers):
    list_of_consumers.append(Consumer(k))

b=0
for j in range(number_of_SIs-1):
    consumer_bin_size=number_of_consumers//number_of_SIs
    # a = random.randint(1, consumer_bin_size-1)
    list_of_SIs.append(SystemIntegrator(unique_id=j, consumer_list=list_of_consumers[b:b+consumer_bin_size]))
    b+=consumer_bin_size
print(b)

list_of_SIs.append(SystemIntegrator(unique_id=number_of_SIs-1, consumer_list=list_of_consumers[b:]))
print(len([len(i.consumers) for i in list_of_SIs]))

for i in range(number_of_ISPs):
    c=0
    list_of_ISPs.append(ISP(unique_id=i, market_share=market_share[i], system_integrator_list=list_of_SIs[c:c+market_share[i]],investment_URLLC=int(conf["investment_URLLC"]), investment_mMTC=int(conf["investment_mMTC"]), URLLC_spectrum_capacity=int(conf["URLLC_spectrum_capacity"]), mMTC_spectrum_capacity=int(conf["mMTC_spectrum_capacity"]), URLLC_infrastructure_cost=int(conf["URLLC_infrastructure_cost"]), mMTC_infrastructure_cost=int(conf["mMTC_infrastructure_cost"])))
    c=10*market_share[i]

City_object = City( isp_list=list_of_ISPs)
# print(len(list_of_consumers[agent_year_update[0]:agent_year_update[0]+agent_year_update[1]]))
for steps in range(1, number_of_steps+1):
    if steps==1:
        for i in list_of_consumers[:agent_year_update[0]]:
            i.if_update=True
    if steps==2:
        for i in list_of_consumers[agent_year_update[0]:agent_year_update[0]+agent_year_update[1]]:
            i.if_update=True
    if steps==3:
        for i in list_of_consumers[agent_year_update[0]+agent_year_update[1]:agent_year_update[0]+agent_year_update[1]+agent_year_update[2]]:
            i.if_update=True
    if steps==4:
        for i in list_of_consumers[agent_year_update[0]+agent_year_update[1]+agent_year_update[2]:agent_year_update[0]+agent_year_update[1]+agent_year_update[2]+agent_year_update[3]]:
            i.if_update=True
    if steps==5:
        for i in list_of_consumers[agent_year_update[0]+agent_year_update[1]+agent_year_update[2]+agent_year_update[3]:agent_year_update[0]+agent_year_update[1]+agent_year_update[2]+agent_year_update[3]+agent_year_update[4]]:
            i.if_update=True
    # count=0

    for consumer in list_of_consumers:
        # if consumer.if_update:
            # count+=1
        consumer.mMTC_scale_later(steps)
        consumer.URLLC_scale_later(steps)
        consumer.cost_later(steps)
        consumer.update_willingness_to_pay(steps)
    # print(count)
    for si in list_of_SIs:
        si.add_investment(steps)

    for isp in list_of_ISPs:
        isp.update_returns()
    
    City_object.update_returns()

for si in list_of_SIs:
    si.create_si_df()

for isp in list_of_ISPs:
    isp.create_isp_df()

City_object.create_city_df()