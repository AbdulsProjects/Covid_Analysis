import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Reading in the tables used
vaccines = pd.read_csv('Vaccinations.csv')
cases_deaths = pd.read_csv('cases_and_deaths_over_time.csv')
pop_char = pd.read_csv('pop_characteristics.csv')
continent_cases = pd.read_csv('cases_by_continent.csv')
continent_deaths = pd.read_csv('deaths_by_continent.csv')


#Creating vaccine graph
#Converting the date column from string to datetime
vaccines['date'] = pd.to_datetime(vaccines['date'], format = '%d/%m/%Y')
#Creating the line chart
f = plt.figure()
f.set_figwidth(10)
plt.plot(vaccines['date'], vaccines['global_vaccinations'])
plt.xlabel('Date')
plt.ylabel('Global Vaccinations')
plt.title('Global Vaccinations over Time')
plt.savefig('Vaccinations.png')


#Creating global cases graph
#Converting the date column from string to datetime
cases_deaths['date'] = pd.to_datetime(vaccines['date'], format = '%d/%m/%Y')
#Creating the line chart
f=plt.figure()
f.set_figwidth(10)
plt.plot(cases_deaths['date'], cases_deaths['cases'])
plt.title('Global Covid-19 Cases over Time')
plt.savefig('Global_Cases.png')


#Creating deaths / death% graph
#Creating the first line plot
fig, ax = plt.subplots()
fig.set_figwidth(15)
line1 = ax.plot(cases_deaths['date'], cases_deaths['deaths'], label = 'Global Deaths')
ax.set_xlabel('Date')
ax.set_ylabel('Global Deaths')

#Creating the second line plot
ax2 = ax.twinx()
line2 = ax2.plot(cases_deaths['date'], cases_deaths['death_percentage'], color='red', label = 'Mortality Percentage (%)')
ax2.set_ylabel('Mortality Percentage (%)')
plt.ylim([0,8])
#Adding both lines into a variable for label extraction
lines = line1 + line2
labels = [l.get_label() for l in lines]
#Creating the figure legend
ax.legend(lines, labels, loc = 7)
ax.set_title('Global Covid-19 Death Statistics')
plt.savefig('Deaths_and_Mortality_Rate.png')


#Creating cases & deaths by continent bar chart
#Refining the dataframe
continent_cases = continent_cases.join(continent_deaths['total_deaths'])
continent_cases = continent_cases.drop('total_cases_per_million', axis = 1)
continent_cases = continent_cases.set_index(['continent'])
#Creating the bar chart
fig = continent_cases.plot(kind = 'bar', secondary_y = 'total_deaths', rot = 0, figsize = (10, 5))
fig.set_ylabel('Total Cases')
fig.right_ax.set_ylabel('Total Deaths')
plt.savefig('by_continent.png')

#Creating heatmap for population characteristics
plt.clf()
plt.figure(figsize = (15, 6))
fig = sns.heatmap(pop_char.corr(), annot = True, cmap = 'BrBG', center = 0)
fig.set_title('Correlation Heatmap')
plt.savefig('pop_characteristics.png')