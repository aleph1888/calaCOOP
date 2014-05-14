#encoding=utf-8

from django_cron import CronJobBase, Schedule

from django.core import mail
from decimal import Decimal
from datetime import datetime
from Invoices.models import Email, EmailNotification
from Invoices.models import Email, EmailNotification, period, PeriodClose, paymentEntities, Soci, SalesInvoice, PurchaseInvoice, periodTaxes

class EmailsNotifierCron(CronJobBase):
	RUN_EVERY_MINS = 0 # every 1 min

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'EmailsNotifierCron' # a unique code

	def do(self):
		#Get all active notificators
		EmailsToSend = EmailNotification.objects.filter(is_active=True)

		connection = mail.get_connection()
		connection.open()
		for yNotifications in EmailsToSend.all():
			#If execution date matches present date
			if yNotifications.execution_date() is datetime.now():
				oneemail = mail.EmailMessage(yNotifications.subject, yNotifications.body, yNotifications.efrom, yNotifications.get_notification_emails_list(), connection=connection)
				oneemail.send()
		
		connection.close()


class PeriodCloseAutomaticClose( CronJobBase ):
	RUN_EVERY_MINS = 0 # every 1 min

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'PeriodCloseAutomaticClose' # a unique code
	
	def do(self):
	
		#All periods already closed
		qs_periods = period.objects.filter( date_close__lt=datetime.now() )
		print "Periods already closed"
		print qs_periods

		for ob_period in qs_periods:
			print "process "
			print ob_period
			
			#For each cooper
			a = 0
			for ob_cooper in Soci.objects.filter(user__is_superuser=False):
				
				if not PeriodClose.objects.filter(period=ob_period, user=ob_cooper.user):
					a = a + 1
					print "cooper: "  
					print ob_cooper
					print " needs automatic close! Procceding..."
					ob_PeriodClose = PeriodClose(period=ob_period, user=ob_cooper.user)
					qs_Sales = SalesInvoice.objects.filter(period=ob_period, user=ob_cooper.user)
					sales_total = sales_invoicedVAT = sales_assignedVAT = sales_totalVAT = Decimal('0.00')
					for item in qs_Sales.all():
						sales_total += item.value
						sales_invoicedVAT += item.invoicedVAT()
						sales_assignedVAT += item.assignedVAT()
						sales_totalVAT += item.total()
				
					ob_PeriodClose.Sales_total = Decimal ( "%.2f" % sales_total )
					ob_PeriodClose.Sales_invoicedVAT = Decimal ( "%.2f" % sales_invoicedVAT )
					ob_PeriodClose.Sales_assignedVAT = Decimal ( "%.2f" % sales_assignedVAT )
					ob_PeriodClose.Sales_totalVAT = Decimal ( "%.2f" % sales_totalVAT )

					qs_Purchase = PurchaseInvoice.objects.filter(period=ob_period, user=ob_cooper.user)
					purchases_total = purchases_expencedVAT = purchases_IRPFRetention = purchases_totalVAT = Decimal('0.00')
					for item in qs_Purchase.all():
						purchases_total += item.value
						purchases_expencedVAT += item.expencedVAT()
						purchases_IRPFRetention += item.IRPFRetention()
						purchases_totalVAT += item.total()

					ob_PeriodClose.Purchases_total = Decimal ( "%.2f" % purchases_total )
					ob_PeriodClose.Purchases_expencedVAT = Decimal ( "%.2f" % purchases_expencedVAT )
					ob_PeriodClose.Purchases_IRPFRetention = Decimal ( "%.2f" % purchases_IRPFRetention )
					ob_PeriodClose.Purchases_totalVAT = Decimal ( "%.2f" % purchases_totalVAT )

					#VATS
					totalVAT1 = Decimal ( "%.2f" % (sales_invoicedVAT - purchases_expencedVAT) )
					if totalVAT1 < 0:
						totalVAT1 = 0
					totalVAT2 = Decimal ( "%.2f" % (sales_assignedVAT - purchases_expencedVAT) )
					if totalVAT2 < 0:
						totalVAT2 = 0
					ob_PeriodClose.VAT_1 =  totalVAT1
					ob_PeriodClose.VAT_2 =  totalVAT2

					#QUOTA
					qs_Tax = periodTaxes.objects.filter(min_base__lte=sales_total, max_base__gte=sales_total)
					value = Decimal('0.00')
					if qs_Tax.count() == 1:
						value = Decimal ( "%.2f" % qs_Tax[0].taxId ) 
					else:
						value = -1
					ob_PeriodClose.periodTAX = value
					ob_PeriodClose.preTAX = ob_cooper.preTAX
					if value > -1:
						print value
						print ob_cooper.preTAX
						value = value - ob_cooper.preTAX
						if value > -1:
							ob_PeriodClose.periodTAXeuro = value
						else:
							ob_PeriodClose.periodTAXeuro = 0
					else:
						ob_PeriodClose.periodTAXeuro = 0
					print " Going to save..."
					ob_PeriodClose.save()
					print " saved!"
			print a
#execute and see log --> python manage.py runcrons 
#see register created in http://localhost:8080/admin/django_cron/cronjoblog/     

