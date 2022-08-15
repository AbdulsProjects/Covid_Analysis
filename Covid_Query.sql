use Covid_Project
go

drop view if exists cases_by_continent, cases_by_country, deaths_by_continent, deaths_by_country, cases_and_deaths_over_time, vaccines, 
cases_and_deaths_over_time_one, pop_characteristics
go

create view cases_by_continent as
(Select continent as continent, max(total_cases) as total_cases, max(total_cases_per_million) as total_cases_per_million
from Covid_Cases
where (continent is not null)
group by continent)
go

create view cases_by_country as
(select location as country, max(total_cases) as total_cases, max(total_cases_per_million) as total_cases_per_million
from Covid_Cases
where continent is not null
group by location)
go

create view deaths_by_continent as
select cd.continent, max(cast(cd.total_deaths as float)) as total_deaths, max(cast(cd.total_deaths_per_million as float)) as total_deaths_per_million, 
(max(cast(cd.total_deaths as float))/max(cc.total_cases))*100 as mortality_percentage 
from Covid_Deaths as cd
inner join cases_by_continent as cc
on cd.continent = cc.continent
group by cd.continent
go

create view deaths_by_country as
select cd.location, max(cast(cd.total_deaths as float)) as total_deaths, max(cast(cd.total_deaths_per_million as float)) as total_deaths_per_million, 
(max(cast(cd.total_deaths as float))/max(cc.total_cases))*100 as mortality_percentage 
from Covid_Deaths as cd
inner join cases_by_country as cc
on cd.location = cc.country
group by cd.location
go

create view vaccines as
with test_vac as 
(select date, sum(cast(new_vaccinations as bigint)) over (order by date) as global_vaccinations
from Population_Info)
select DISTINCT date, global_vaccinations 
from test_vac
go

create view cases_and_deaths_over_time as
select cc.date, SUM(cc.total_cases) as cases, SUM(cast(cd.total_deaths as int)) as deaths, 
(SUM(cast(cd.total_deaths as int)) / SUM(cc.total_cases) * 100) as death_percentage, global_vaccinations
from Covid_Cases as cc
inner join Covid_Deaths as cd
on cc.date = cd.date and cc.location = cd.location
inner join vaccines
on vaccines.date = cc.date
group by cc.date, global_vaccinations
go

create view pop_characteristics as
select pop.location, avg(stringency_index) as avg_stringency_index, population_density as population_density, median_age as median_age, cardiovasc_death_rate as cadriovasc_death_rate,
mortality_percentage
from Population_Info as pop
inner join deaths_by_country as dbc
on dbc.location = pop.location
where continent is not null
group by pop.location, population_density, median_age, cardiovasc_death_rate, mortality_percentage
go

select * from cases_and_deaths_over_time
order by date
