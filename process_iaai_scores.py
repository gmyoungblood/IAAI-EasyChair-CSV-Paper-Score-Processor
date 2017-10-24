#-----------------------------------------------------------------------------------------
# IAAI EasyChair CSV Paper Score Processor
# (CC BY-SA 4.0) 2016
# by G. Michael Youngblood, Ph.D. (GMY) <gmyoungblood@gmail.com>
# and ...
#-----------------------------------------------------------------------------------------
# If you don't like this code, you are welcome to re-write it. It is not optimized.
# It is a quick and dirty process to process the data output by EasyChair. It does the job 
# and minimal thought and overhead were put into it. I essentially wrote it in an hour or so
# while sitting in a meeting that I probably should have been paying attention to. 
#-----------------------------------------------------------------------------------------
# HISTORY:
#	10-19-2016: (GMY) Original Version
#	10-20-2016: (GMY) Added output column in spreadsheet for number of reviews. 
#                     Added issues information to output.
#	10-20-2016: (GMY) Added paper classification and the req that Challenge Papers be defined
#-----------------------------------------------------------------------------------------
# LICENSE: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) 
#
# You are free to:
# Share - copy and redistribute the material in any medium or format
# Adapt - remix, transform, and build upon the material for any purpose, even commercially.
# 
# The licensor cannot revoke these freedoms as long as you follow the license terms.
# 
# Under the following terms:
# Attribution - You must give appropriate credit, provide a link to the license, and 
#   indicate if changes were made. You may do so in any reasonable manner, but not in any 
#   way that suggests the licensor endorses you or your use.
# ShareAlike - If you remix, transform, or build upon the material, you must distribute 
#   your contributions under the same license as the original.
# 
# No additional restrictions - You may not apply legal terms or technological measures 
#   that legally restrict others from doing anything the license permits.
#
# Notices:
# You do not have to comply with the license for elements of the material in the public 
# domain or where your use is permitted by an applicable exception or limitation.
#
# No warranties are given. The license may not give you all of the permissions necessary 
# for your intended use. For example, other rights such as publicity, privacy, or moral 
# rights may limit how you use the material.
#
#-----------------------------------------------------------------------------------------
import csv
review_file =  'review.csv'
score_file  =  'review_score.csv'
output_file =  'iaai_scoring_output.csv'
REVIEW_MIN = 3
challenge_papers = [52, 63, 75, 84]

# This is just a linear script execution in Python, so processing starts here 
# (no main, no functions, no objects, no mess, no fuss, get over yourself)
# Ok, start!

# Introduction output
#
print '\nIAAI EasyChair CSV Paper Score Processor'
print '----------------------------------------'
print ' Processing review number mapping file: ' + review_file
print ' with the scores file: ' + score_file

# Create a dictionary of review numbers to submission numbers
# This mapping is found in the review file, so we will grab them from there
#
paper_dict = {}
with open(review_file, 'rb') as review:
	review_reader = csv.reader(review, delimiter=',', quotechar='|')
	row_count = 0
	for row in review_reader:
		if len(row) > 1 and row[0].isdigit():
			paper_dict[row[0]] = {'paper' : int(row[1])}
			# print 'Storing ' + str(row[0]) + ' : ' + str(row[1])
		row_count += 1
		
# Debug to find specific number of reviews for a paper
#
#for item in paper_dict:
#	if paper_dict[item]['paper'] == 55:
#		print str(item) + ' : ' + str(paper_dict[item])

# Pull in the individual scores for each paper
#
#
with open(score_file, 'rb') as review_score:
	review_score_reader = csv.reader(review_score, delimiter=',', quotechar='|')
	row_count = 0
	for row in review_score_reader:
		if row_count > 0 and row[2] != '' and row[0].isdigit():
			# print ', '.join(row)
			try:
				# print paper_dict[str(row[0])]
				list = paper_dict[row[0]]
			except KeyError:
				# print "Missing associated review for %d" % int(row[0])
				# This appears to be an EasyChair problem, which is likely due to deleted and replaced reviews
				continue
			if int(row[1]) != 17:
				list.update({int(row[1]) : int(row[2])})
			else:
				if row[2] == 'yes':
					list.update({int(row[1]) : 1})
				else:
					list.update({int(row[1]) : 0})
		row_count += 1


# Debug: Intermediate check
#
# print paper_dict
#
## or this for the specific papers
#
new_list = sorted(paper_dict.values())
item_count = 0
for i in new_list:
	# print i['paper']
	item_count += 1
print ' There are ' + str(item_count) + ' paper reviews.' 


# Main score processor --
#
# Let's plan to output info for each paper along the way
with open(output_file, 'wb') as outfile:
	outwriter = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	outwriter.writerow(['Paper', 'Significance', 'AI Technology', 'Innovation', 
			'Content', 'Technical Quality', 'Clarity', 'Integrated Systems', 'Evaluation (Emerging Only)',
			'Task or Problem Description*', 'Application Description*', 
			'Uses of AI Technology*', 'Application Use and Payoff*', 
			'Application Development and Deployment*', 'Maintenance*',
			'Overall Average', 'Recommendation', 'AI Magazine Nomination', 'Number of Reviews', 'Classification'])
			
	# For each paper, find all of the reviews, add them to a local dictionary
	history = []
	missing_review_count = 0
	missing_review_papers = []
	missing_score_papers = []
	emerging_papers = []
	deployed_papers = []

	for item in sorted(paper_dict.values()):
		# Get paper in focus
		paper = item['paper']
		#print 'Focus on paper: ' + str(paper)
		if paper not in history:
			#print 'Searching for paper ' + str(paper)
			history.append(paper)
			#print 'HISTORY: '
			#print history
			# Now find and build a set of reviews for this paper
			dict_list = []
			review_count = 0
			for each_item in sorted(paper_dict.values()):
				if each_item['paper'] == paper:
					review_count += 1
					#print each_item
					dict_list.append(each_item)
			print ' For paper  ' + str(paper) + '  found  ' + str(review_count) + '  reviews' + ('.' if (review_count >= REVIEW_MIN) else ', which is below the minimum.')
			missing_review_count += REVIEW_MIN - review_count
			
			# Track missing review papers
			if (review_count < REVIEW_MIN):
				missing_review_papers.append(paper)
			#print dict_list
			
			# Process the local dictionary list and prepare output
			# 1 = Significance
			# 2 = AI Technology
			# 3 = Innovation
			# 4 = Content
			# 5 = Technical Quality
			# 6 = Clarity
			# 7 = Integrated Systems
			# 8 = Evaluation (Emerging Only)
			# 9 = Task or Problem Description
			# 10 = Application Description
			# 11 = Uses of AI Technology
			# 12 = Application Use and Payoff
			# 13 = Application Development and Deployment
			# 14 = Maintenance
			# Overall Average (calculated)
			# 16 = Recommendation
			# 17 = AI Magazine Nomination
			instances = 0
			sig = tech = inno = content = tqual = clarity = eval = i_sys = 0.0
			task = appd = uses = payoff = deploy = maint = 0.0
			overall = recommendation = mag = 0.0
			
			# Setup output file
			#    This could be made a lot more generic by using an array, etc., but this
			#  afforded me a completely transparent way to work with these variables and test
			
			score_missing = False
			
			# Process scores and ouput
			for scores in dict_list:
				try:
					sig += scores[1]
				except KeyError:
					sig += 0.0
					print '     !!! Paper ' + str(paper) + ' missing Significance score !!!'
					score_missing = True
				
				try:
					tech += scores[2]
				except KeyError:
					tech += 0.0
					print '     !!! Paper ' + str(paper) + ' missing AI Technology score !!!'
					score_missing = True
				
				try:
					inno += scores[3]
				except KeyError:
					inno += 0.0
					print '     !!! Paper ' + str(paper) + ' missing Innovation score !!!'
					score_missing = True
				
				try:
					content += scores[4]
				except KeyError:
					content += 0.0
					print '     !!! Paper ' + str(paper) + ' missing Content score !!!'
					score_missing = True
					
				try:
					tqual += scores[5]
				except KeyError:
					tqual += 0.0	
					print '     !!! Paper ' + str(paper) + ' missing Technical Quality score !!!'
					score_missing = True
					
				try:
					clarity += scores[6]
				except KeyError:
					clarity += 0.0
					print '     !!! Paper ' + str(paper) + ' missing Clarity score !!!'
					score_missing = True

				try:
					i_sys += scores[7]
				except KeyError:
					i_sys += 0.0

				try:
					eval += scores[8]
				except KeyError:
					eval += 0.0
					
				try:
					task += scores[9]
				except KeyError:
					task += 0.0
					
				try:
					appd += scores[10]
				except KeyError:
					appd += 0.0
					
				try:
					uses += scores[11]
				except KeyError:
					uses += 0.0
					
				try:
					payoff += scores[12]
				except KeyError:
					payoff += 0.0
					
				try:
					deploy += scores[13]
				except KeyError:
					deploy += 0.0
					
				try:
					maint += scores[14]
				except KeyError:
					maint += 0.0
					
				try:
					recommendation  += scores[16]
				except KeyError:
					recommendation += 0.0
					print '     !!! Paper ' + str(paper) + ' missing Recommendation !!!'
					score_missing = True
				try:
					mag += scores[17]
				except KeyError:
					mag += 0.0
					print '     !!! Paper ' + str(paper) + ' missing AI Magazine recommendation !!!'
					score_missing = True
					
				instances += 1
				
				# Error checks
				# Emerging Paper Idiot checks
				if (task == 0.0 and appd == 0.0 and uses == 0.0 and payoff == 0.0 and deploy == 0.0 and maint == 0.0):
					if (eval == 0.0):
						if paper not in challenge_papers:
							print '     !!! Paper ' + str(paper) + ' missing Eval score for Emerging Paper !!!'
							score_missing = True
				# Deployed Paper Idiot Checks
				else:
					if (eval > 0.0):
						print '     !!! Paper ' + str(paper) + ' has Eval score for a Deployed Paper !!!'
					if (task == 0.0):
						print '     !!! Paper ' + str(paper) + ' missing Task score for Deployed Paper !!!'
						score_missing = True
					if (appd == 0.0):
						print '     !!! Paper ' + str(paper) + ' missing App Description score for Deployed Paper !!!'
						score_missing = True
					if (uses == 0.0):
						print '     !!! Paper ' + str(paper) + ' missing Uses score for Deployed Paper !!!'
						score_missing = True
					if (payoff == 0.0):
						print '     !!! Paper ' + str(paper) + ' missing Payoff score for Deployed Paper !!!'
						score_missing = True
					if (deploy == 0.0):
						print '     !!! Paper ' + str(paper) + ' missing Deployment score for Deployed Paper !!!'
						score_missing = True
					if (maint == 0.0):
						print '     !!! Paper ' + str(paper) + ' missing Maintenance score for Deployed Paper !!!'
						score_missing = True
					
				
			sig /= instances
			tech /= instances
			inno /= instances
			content /= instances
			tqual /= instances
			clarity /= instances
			i_sys /= instances
			eval /= instances
			task /= instances
			appd /= instances
			uses /= instances
			payoff /= instances
			deploy /= instances
			maint /= instances
			recommendation /= instances
			mag /= instances
			
			if score_missing:
				missing_score_papers.append(paper)

			classification = 'unknown'
			
			# Calculate Overall
			if paper in challenge_papers:
				# Challenge
				overall = (sig + tech + inno + content + tqual + clarity) / 6.0
				classification = 'challenge'
			elif eval > 0.0 and maint == 0.0:
				# Emerging
				overall = (sig + tech + inno + content + tqual + clarity + eval) / 7.0
				emerging_papers.append(paper)
				classification = 'emerging'
			else:
				# Deployed
				overall = (sig + tech + inno + content + tqual + clarity + task + appd + uses + payoff + deploy + maint) / 12.0
				deployed_papers.append(paper)
				classification = 'deployed'
			
			out_list = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'unclassified']
			out_list[0] = paper
			out_list[1] = sig
			out_list[2] = tech
			out_list[3] = inno
			out_list[4] = content
			out_list[5] = tqual
			out_list[6] = clarity
			out_list[7] = i_sys
			out_list[8] = eval
			out_list[9] = task
			out_list[10] = appd
			out_list[11] = uses
			out_list[12] = payoff
			out_list[13] = deploy
			out_list[14] = maint
			out_list[15] = overall
			out_list[16] = recommendation
			out_list[17] = mag
			out_list[18] = instances
			out_list[19] = classification
			outwriter.writerow(out_list)
		
unique_papers = len(history)
print '----------------------------------------'
print ' There are ' + str(unique_papers) + ' unique papers.'
print ' There are ' + str(missing_review_count) + ' missing reviews.'
print ' There is an average of ' + str(float(item_count)/float(unique_papers))+ ' reviews per paper.'
print ' Issues:'
print '   Papers with missing reviews: ' + str(sorted(missing_review_papers))
print '   Papers with missing scores: ' + str(sorted(missing_score_papers))
print ' Papers:'
print '   Challenge Papers: ' + str(challenge_papers)
print '   Deployed Papers: ' + str(sorted(deployed_papers))
print '   Emerging papers: ' + str(sorted(emerging_papers))
print '----------------------------------------'
print ' Processing complete.\n'
# fin.
