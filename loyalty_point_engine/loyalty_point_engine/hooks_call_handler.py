# Copyright (c) 2013, Saurabh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from erpnext.accounts.party import create_party_account
from frappe import _
from frappe.utils import cint
from loyalty_point_engine.loyalty_point_engine.engine import initiate_point_engine
from loyalty_point_engine.loyalty_point_engine.accounts_handler import create_account_head

def create_acc_payable_head(doc, method):
	if not doc.get('__islocal') and doc.get('__islocal') != None:
		create_account_head(doc)

def grab_invoice_details(doc, method):
	point_validation(doc)
	initiate_point_engine(doc)

def point_validation(doc):
	limit_exceed(doc.total_earned_points, doc.redeem_points)

def limit_exceed(earned_points, redeem_points):
	if redeem_points > earned_points:
		frappe.msgprint(" Redeemption limit exceeded ", raise_exception=1)

def referral_management(doc, method):
	""" create lead if referral is not customer"""

@frappe.whitelist()
def get_points(customer):
	points = frappe.db.sql("""select sum(points) from `tabPoint Transaction` where customer = '%s'"""%(customer), as_list=1)
	return {
		"points": ((len(points[0]) > 1) and points[0] or points[0][0]) if points else None
	}