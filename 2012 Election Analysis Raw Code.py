###############################################################################################################################
# Arsal Munawar
# Analysis and Visualization of 2012 Election Data
# the following code is to be run in Jupyter notebook but can be run in other environments

# The following questions regarding the 2012 election between Barack Obama and Mitt Romney will be answered:
# 1. Who was being polled and what was their party affiliation?
# 2. Did the poll results favor Romney or Obama?
# 3. How do undecided voters effect the poll?
# 4. Can we account for the undecided voters?
# 5. How did voter sentiment change over time?
# 6. Can we see an effect in the polls from the debates?

# After that, the following questions regarding donations to the campaigns will be answered:
# 7. How much was donated and what was the average donation?
# 8. How did the donations differ between candidates?
# 9. How did the donations differ between Democrats and Republicans?
# 10. What were the demographics of the donors?
# 11. Is there a pattern to donation amounts?

###############################################################################################################################
# first lets import all necessary packages and import the first data set

# import the data handling packages
import numpy as np
import pandas as pd
from pandas import Series,DataFrame

# import the data visualization packages, and lets make sure the plots show up and have white grid backgrounds
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
%matplotlib inline

# use __future__ to allow us to use proper division with floats
from __future__ import division

# requests is imported to gather data from the web
import requests

# StringIO will make it easier to read csv data
from StringIO import StringIO

# this is the URL where the data exists
url = "http://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama.csv"

# this will convert the information into text form
source = requests.get(url).text
poll_data = StringIO(source)

# this will turn the data into a dataframe
poll_df = pd.read_csv(poll_data)

###############################################################################################################################
# now lets take a glance at the data, the column, the data types, and if there are any incomplete data points, etc

# lets see the columns info
poll_df.info()
# looking at the info, we can see that there are 586 rows and 17 columns of varying data types. some columns have 
# incomplete entries

# lets take a look at the first 10 rows of the data set
poll_df.head(10)
# based on quick observations, any NaN values in the 'other' or 'undecided' columns can be set to 0. The other
# column which contain NaN values will be dealt with if needed.

# it's also good practice to look at the last 10 rows of data as well
poll_df.tail(10)
# note that the polls were conducted over the course of a few years, with the earliest polls being in March 2009 and 
# the latest polls being just days before the election.

###############################################################################################################################
# 1. lets get to answering the first question. Who was being polled and what was their party affiliation?

# lets see who was being polled. this will give us the count for each unique entry in the column, and will create
# a barchart
sns.countplot('Population',data=poll_df)
poll_df['Population'].value_counts()
# the pollees consisted of likely voters, registered voters, and adults. In others words, people who have an interest
# in politics or are affected by decisions made by politicians. its important to use both lines of code above to get
# the count plot and the actual count

# now lets see the party affiliation of the poll sites.
sns.countplot('Affiliation',data=poll_df,palette=['grey','red','blue','yellow'])
poll_df['Affiliation'].value_counts()
# most polls were neither Democractic or Republican, but still there were far more dems than reps. This is potentially
# sampling bias and could skew the poll results that we see ahead

# lets combine both the population and affiliation into one graph to see what we can find. the party affiliation
# is the x-axis, and is varied by the population
sns.countplot('Affiliation',data=poll_df,hue='Population')
# the un-affiliated polls had the highest number of registered and likely voters

# another graph, but with affliation and population switched
sns.set_style('whitegrid')
sns.countplot('Population',data=poll_df,hue='Affiliation',palette=['grey','red','blue','yellow'])
# most of the pollees were casting their opinions on un-affiliated polls, which is good.

# In summary, most pollees were likely or registered voters, and most poll sites were unaffiliated, but some were
# democratic. now that we know who was being polled and the poll affiliations, lets move on to the next question.

###############################################################################################################################
# 2. lets find out if the polls favored Obama or Romney

# lets first find the average poll response for Obama, Romney, Other, and Undecided. lets also remove te columns which
# we do not need to see using .drop()
avg = pd.DataFrame(poll_df.mean())
avg.drop(['Number of Observations','Question Text','Question Iteration'], axis=0, inplace=True)
avg #or 'print(avg)' if using a traditional environment
# we can see that on average, Obama was favored over Romney by just 2.2 points.

# lets find the standard deviation of those poll numbers
std = pd.DataFrame(poll_df.std())
std.drop(['Number of Observations','Question Text','Question Iteration'], axis=0, inplace=True)
std #or 'print(std)' if using a traditional environment
# not only was Obama favored in the polls, but also had a smaller variation between the polls than Romney. Obama was
# the steady favorite.

# lets create a bar chart of the mean with the std being the error on the y-axis
avg.plot(yerr=std,kind='bar',legend=False)
# the undecided voters make up a decent chunk, roughly 7%. they will have a big impact on the election results.
# this leads us to our next question.

###############################################################################################################################
# 3,4,5. lets see how undecided voters effect the poll, and how voter sentiment changed over time

# first lets combine the avg and std charts for easier comparison, and lets rename the columns.
poll_avg = pd.concat([avg,std],axis=1)
poll_avg.columns = ['Average','STD']
poll_avg

# we will create a crude time-series graph of voter sentiment for all polls, to see how opinions changed as election
# time came closer. the initial plot is in reverse time-order, so we must invert the x-axis
time_series = poll_df.plot(x='End Date', y=['Obama','Romney','Undecided'],marker='o',linestyle='',figsize=(10,5))
time_series.invert_xaxis()
# the plot shows that voters who were initially undecided eventually made decisions. we can also see the gap in
# voter sentiment between Obama and Romney close towards the election date. this gives us a quick idea, but
# lets get more specific.

# lets find the poll difference between Obama and Romney by using data we already have. well create a new column
# in the databse.
poll_df['Difference'] = (poll_df.Obama - poll_df.Romney)/100
poll_df['Difference'].head
# a positive difference means Obama is favored, and a negative difference means Romney is favored

# lets plot the difference over time
poll_diff = poll_df.plot(x='End Date', y=['Difference'],marker='o',linestyle='',figsize=(10,5))
poll_diff.invert_xaxis()
# we can see that the difference in poll scores decreases with time.

# to get a clearer picture on the difference over time, lets group the polls by start date and display the data.
# we will display the data by group date, and in particular we will show the mean difference for each start date
poll_df = poll_df.groupby(['Start Date'], as_index=False).mean()
poll_df.head()

# now lets plot the start date and mean difference to better visualize the above graph
diff_plot = poll_df.plot(x='Start Date', y='Difference', marker='o', linestyle='-', figsize=(12,5))
# this is a slightly clearer graph from before, highlighting the same trend.

###############################################################################################################################
# 6. Can we see an effect in the polls from the debates?

# the debates occured on October 3, 16, 22 of 2012. Lets see if the debates changed the polls in any way. first lets
# find the exact dates on the time series that the debates occured, then we'll plot vertical lines on those dates to
# clearly see the cange before and after the debates.

# this is a loop that will determine all of the indexes which include October 2012 as the start date. We will plot
# the index range so we can see all poll resutls from October 2012. We can also do this by simply sorting the
# dataframe and manually checking the indexes, but this will not be useful for large dataframes or for instances
# in which specific rows must be found. So it is useful to create a loop to be able to do this for future use.
row_index = 0
xlimit = []
oct_day = []

for date in poll_df['Start Date']:
    if date[0:7] == '2012-10':
        xlimit.append(row_index)
        row_index += 1
        oct_day.append(date)
    else:
        row_index += 1


count = 0
for x in xlimit:
    print xlimit[count],oct_day[count]
    count += 1
# we can see that the October 2012 is between indexes 325 and 352. these will be the limits of our graph
# of the debate dates. we can also see the exact days in October next to those indexes.

# using our plot of start time and difference, we add the x-axis limits and plot again
diff_plot = poll_df.plot(x='Start Date', y='Difference', marker='o', linestyle='-', figsize=(12,5),
                         xlim=(min(xlimit),max(xlimit)))

# lets add vertical lines to the dates of the debates. we know exactly what indexes the debates are.
# For October 3 there is no poll, so we will plot a vertical line for the next date which is 10/4 and
# an index of 327. For the 10/16 and 10/22 debates, we will use 338 and 343 indexes, respectively
plt.axvline(x=327, linewidth=4, color='yellow')
plt.axvline(x=338, linewidth=4, color='yellow')
plt.axvline(x=343, linewidth=4, color='yellow')
# these lines make it easy to see the reaction after the debates. After the first debeate, voter
# sentiment shifted towards Obama, but the opposite trend occured after the second debate. The third
# debate didn't change sentiment much, perhaps because voters had alraedy decided based on the first
# two debates.

###############################################################################################################################
# lets find out more about the donor dataset. first lets import the dataset and explore it

donor_df = pd.read_csv("Election Donor Data.csv")
donor_df.info()
donor_df.describe()
# there are over 1 million rows and 16 columns of donor information, which candidate the donations were for, the date
# of the donations, and more information.

#7. How much was donated and what was the average donation?
donor_df['contb_receipt_amt'].sum()
donor_df['contb_receipt_amt'].mean()
donor_df['contb_receipt_amt'].describe()
donor_df['contb_receipt_amt'].value_counts()
# the total amount donated was $298,751,395, and the average donation was $298. a donation of just $100 puts you
# ahead of 50% of the donors, but $2500 puts you ahead of 75% of the people. The largest donation was over $2,000,000
# while the lowest was a negative number, maybe the respective campaigns donated to other campaigns? There were over
# 8,000 different amounts of donations, and the standard deviation of the donations was $3749. That is a high variation,
# which means there were some very low and very high donations which muddy the picture.

# lets make a dataframe of just the contribution amounts
top_donor = donor_df['contb_receipt_amt'].copy()
top_donor.sort_values()
# now all donation values are sorted. we can see that there are only 7 donations over $34,000, and these 7 are all above
# $450,000. There are over a million donation records, so although these 7 are large compared to the rest, they probably
# do not have much of an impact on the mean of 298. The negative donation amounts are refunds to donors.

# lets take a look at only the donations above zero, so no refunds.
top_donor = top_donor[top_donor > 0]
# there were 991475 positive contributions

# lets sort this list, and see the 10 most common donation amounts
top_donor.sort_values()
top_donor.value_counts().head(10)
# the 10 most commonn donation amounts ranged from 10 to 2500 dollars, with the most common being 100, and 50 and 25
# after that.

# are donations usually made in even amounts like 100, 250, 1000, etc? lets find out
donation_counts = top_donor[top_donor < 2500]
donation_counts.hist(bins=100,linewidth=1,figsize=(10,4))
# we can see that yes, donations are usually made in even numbers based on the spikes of the histograms

###############################################################################################################################
# 8. How did the donations differ between candidates?

# lets sort the donations based on party, but first we have to create a party column
candidates = donor_df.cand_nm.unique()
# from this list, Obama is the only democrat

# lets make a dictionary to organize the party affiliations
party_map = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}

# now make a column in the donor_df of the party dictionary. notice how we are mapping the values of the
# cand_nm column to the new party map column
donor_df['Party'] = donor_df.cand_nm.map(party_map)

# lets clear all the refunds in the contribution column as well
donor_df = donor_df[donor_df.contb_receipt_amt > 0]

# now we can see which candidate had the most donors, and the amount of donations
donor_df.groupby('cand_nm')['contb_receipt_amt'].count()
donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()
# we can see that Obama had the most donors, as he was the only Democrat and had no competition, unlike the
# republicans. we can also see that Obama had the largest monetary value of donations

# to make the values more readable
cand_amount = donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()
i = 0

for don in cand_amount:
    print " The candidate %s raised %.0f dollars " %(cand_amount.index[i],don)
    print '\n'
    i += 1

# lets create a bar chart of donations amounts among the candidates, this will be much easier to read
cand_amount.plot(kind='bar')

###############################################################################################################################
# 9. How did the donations differ between Democrats and Republicans?

# lets make another bar chart comparing the Democartic and Republican party donations
donor_df.groupby('Party')['contb_receipt_amt'].sum().plot(kind='bar',color=['blue','red'])
# The Republicans raised more than the Democrats, but their donations were split maongst all their
# candidates unlike the Democratic party.

###############################################################################################################################
# 10. What were the demographics of the donors?

# Use a pivot table to extract and organize the data by the donor occupation
occupation_df = donor_df.pivot_table('contb_receipt_amt', index='contbr_occupation', columns='Party', aggfunc='sum')

# lets see the shape of the dataframe to get an idea
occupation_df.shape
# its (45067, 2)

# lets limit the table to make it manageable and only see the large sums of donations by occupation
occupation_df = occupation_df[occupation_df.sum(1) > 1000000]
occupation_df.shape()
# this is much smaller, (31,2) shape

# lets plot the new df
occupation_df.plot(kind='barh',figsize=(10,12),cmap='seismic')
# Looks like there are some occupations that are either mislabeled or aren't really occupations.
# Let's get rid of: Information Requested occupations and let's combine CEO and C.E.O.
occupation_df.drop(['INFORMATION REQUESTED PER BEST EFFORTS','INFORMATION REQUESTED'],axis=0,inplace=True)

# Set new ceo row as sum of the current two
occupation_df.loc['CEO'] = occupation_df.loc['CEO'] + occupation_df.loc['C.E.O.']
# Drop CEO
occupation_df.drop('C.E.O.',inplace=True)

# lets now replot the graph and visualize the donations
occupation_df.plot(kind='barh',figsize=(8,12),cmap='seismic')

###############################################################################################################################
# 11. Is there a pattern to donation amounts?

# Repeat previous plot!
occupation_df.plot(kind='barh',figsize=(10,12),cmap='seismic')
# Looks like CEOs are a little more conservative leaning, this may be due to the tax philosphies
# of each party during the election.