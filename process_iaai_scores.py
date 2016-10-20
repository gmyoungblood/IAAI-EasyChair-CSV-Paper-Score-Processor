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
#	10-19-2016: GMY: Original Version
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
		if row_count > 0 and len(row) > 1 and row[0].isdigit():
			paper_dict[row[0]] = {'paper' : int(row[1])}
			#print 'Storing ' + str(row[0]) + ' : ' + str(row[1])
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
			#print ', '.join(row)
			#print paper_dict[str(row[0])]
			list = paper_dict[str(row[0])]
			if int(row[1]) != 16:
				list.update({int(row[1]) : int(row[2])}) 
			else:
				if row[2] == 'yes':
					list.update({int(row[1]) : 1}) 
				else:
					list.update({int(row[1]) : 0}) 
		row_count += 1

# Debug: Intermediate check
#
#print paper_dict
#
## or this for the specific papers
#
new_list = sorted(paper_dict.values())
item_count = 0
for i in new_list:
#	print i['paper']
	item_count += 1
print ' There are ' + str(item_count) + ' paper reviews.' 

# Main score processor --
#
# Let's plan to output info for each paper along the way
with open(output_file, 'wb') as outfile:
	outwriter = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	outwriter.writerow(['Paper', 'Significance', 'AI Technology', 'Innovation', 
			'Content', 'Technical Quality', 'Clarity', 'Evaluation (Emerging Only)', 
			'Task or Problem Description*', 'Application Description*', 
			'Uses of AI Technology*', 'Application Use and Payoff*', 
			'Application Development and Deployment*', 'Maintenance*',
			'Overall Average', 'Recommendation', 'AI Magazine Nomination'])
			
	# For each paper, find all of the reviews, add them to a local dictionary
	history = []
	missing_review_count = 0

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
			#print dict_list
			
			# Process the local dictionary list and prepare output
			# 1 = Significance
			# 2 = AI Technology
			# 3 = Innovation
			# 4 = Content
			# 5 = Technical Quality
			# 6 = Clarity
			# 7 = Evaluation (Emerging Only)
			# 8 = Task or Problem Description
			# 9 = Application Description
			# 10 = Uses of AI Technology
			# 11 = Application Use and Payoff
			# 12 = Application Development and Deployment
			# 13 = Maintenance
			# Overall Average (calculated)
			# 15 = Recommendation
			# 16 = AI Magazine Nomination
			instances = 0
			sig = tech = inno = content = tqual = clarity = eval = 0.0
			task = appd = uses = payoff = deploy = maint = 0.0
			overall = recommendation = mag = 0.0
			
			# Setup output file
			#    This could be made a lot more generic by using an array, etc., but this
			#  afforded me a completely transparent way to work with these variables and test

			# Process scores and ouput
			for scores in dict_list:
				try:
					sig += scores[1]
				except KeyError:
					sig += 0.0
					print '!!! Paper ' + str(paper) + ' missing Significance score !!!'
				
				try:
					tech += scores[2]
				except KeyError:
					tech += 0.0
					print '!!! Paper ' + str(paper) + ' missing AI Technology score !!!'
				
				try:
					inno += scores[3]
				except KeyError:
					inno += 0.0
					print '!!! Paper ' + str(paper) + ' missing Innovation score !!!'
				
				try:
					content += scores[4]
				except KeyError:
					content += 0.0
					print '!!! Paper ' + str(paper) + ' missing Content score !!!'
					
				try:
					tqual += scores[5]
				except KeyError:
					tqual += 0.0	
					print '!!! Paper ' + str(paper) + ' missing Technical Quality score !!!'
					
				try:
					clarity += scores[6]
				except KeyError:
					clarity += 0.0
					print '!!! Paper ' + str(paper) + ' missing Clarity score !!!'
				
				try:
					eval += scores[7]
				except KeyError:
					eval += 0.0
					
				try:
					task += scores[8]
				except KeyError:
					task += 0.0
					
				try:
					appd += scores[9]
				except KeyError:
					appd += 0.0
					
				try:
					uses += scores[10]
				except KeyError:
					uses += 0.0
					
				try:
					payoff += scores[11]
				except KeyError:
					payoff += 0.0
					
				try:
					deploy += scores[12]
				except KeyError:
					deploy += 0.0
					
				try:
					maint += scores[13]
				except KeyError:
					maint += 0.0
					
				try:
					recommendation  += scores[15]
				except KeyError:
					recommendation += 0.0
					print '!!! Paper ' + str(paper) + ' missing Recommendation !!!'
				try:
					mag += scores[16]
				except KeyError:
					mag += 0.0
					print '!!! Paper ' + str(paper) + ' missing AI Magazine recommendation !!!'
					
				instances += 1
				
				# Error checks
				# Emerging Paper Idiot checks
				if (task == 0.0 and appd == 0.0 and uses == 0.0 and payoff == 0.0 and deploy == 0.0 and maint == 0.0):
					if (eval == 0.0):
						print '!!! Paper ' + str(paper) + ' missing Eval score for Emerging Paper !!!'
				# Deployed Paper Idiot Checks
				else:
					if (eval > 0.0):
						print '!!! Paper ' + str(paper) + ' has Eval score for a Deployed Paper !!!'
					if (task == 0.0):
						print '!!! Paper ' + str(paper) + ' missing Task score for Deployed Paper !!!'
					if (appd == 0.0):
						print '!!! Paper ' + str(paper) + ' missing App Description score for Deployed Paper !!!'
					if (uses == 0.0):
						print '!!! Paper ' + str(paper) + ' missing Uses score for Deployed Paper !!!'
					if (payoff == 0.0):
						print '!!! Paper ' + str(paper) + ' missing Payoff score for Deployed Paper !!!'
					if (deploy == 0.0):
						print '!!! Paper ' + str(paper) + ' missing Deployment score for Deployed Paper !!!'
					if (maint == 0.0):
						print '!!! Paper ' + str(paper) + ' missing Maintenance score for Deployed Paper !!!'
					
				
			sig /= instances
			tech /= instances
			inno /= instances
			content /= instances
			tqual /= instances
			clarity /= instances
			eval /= instances
			task /= instances
			appd /= instances
			uses /= instances
			payoff /= instances
			deploy /= instances
			maint /= instances
			recommendation /= instances
			mag /= instances
			
			# Calculate Overall
			if eval > 0.0:
				# Emerging
				overall = (sig + tech + inno + content + tqual + clarity + eval) / 7.0
			else:
				# Deployed
				overall = (sig + tech + inno + content + tqual + clarity + task + appd + uses + payoff + deploy + maint) / 12.0
			
			out_list = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
			out_list[0] = paper
			out_list[1] = sig
			out_list[2] = tech
			out_list[3] = inno
			out_list[4] = content
			out_list[5] = tqual
			out_list[6] = clarity
			out_list[7] = eval
			out_list[8] = task
			out_list[9] = appd
			out_list[10] = uses
			out_list[11] = payoff
			out_list[12] = deploy
			out_list[13] = maint
			out_list[14] = overall
			out_list[15] = recommendation
			out_list[16] = mag
			outwriter.writerow(out_list)
		
unique_papers = len(history)
print ' There are ' + str(unique_papers) + ' unique papers.'
print ' There are ' + str(missing_review_count) + ' missing reviews.'
print ' There is an average of ' + str(float(item_count)/float(unique_papers))+ ' reviews per paper.'

print ' Processing complete.\n'
# fin.
