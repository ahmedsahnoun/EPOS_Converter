from xml.etree import ElementTree as ET

class OPI_ZVT_Converter:

	def convert(self,x):
		try:
			root = ET.fromstring(x)
			if root != None:
				result = self.dictionary(root)
				if result == "x2":
					result = "Option non supportée"
		except:
			result = "Entrée non valide"
		return(result)

	def dictionary(self,root):
		
		result = ""

		xmlns="/{http://www.nrf-arts.org/IXRetail/namespace}/"
		
		if root.tag == '{http://www.nrf-arts.org/IXRetail/namespace}ServiceRequest':
		# if root.tag == '{http://www.nrf-arts.org/IXRetail/namespace}CardServiceRequest':
			if root.attrib['RequestType'] == 'Login':
				result = "0600" 				#tag
				result += "000000"			#password
				result += "04"					#config byte
				result += "0978"				#cc
				result += "03"					#service byte*

			if root.attrib['RequestType'] == 'CardPayment':
				result = "0601" 				#tag
				x = root.find("." + xmlns + "TotalAmount").text
				x = hex(int(x))[2:]
				result += "04" + x 			#amount
				result += "490978" 			#cc
				result += "1902" 				#payment type
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track1" + xmlns + "Byte")
				if x != None : result += "2D" + x.text				#track 1
				x = root.find("." + xmlns + "CardValue" + xmlns + "ExpiryDate")
				if x != None : result += "0E" + x.text 			#expiry date
				x = root.find("." + xmlns + "CardValue" + xmlns + "CardPAN")
				if x != None : result += "22" + x.text			 	#card number
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track2" + xmlns + "Byte")
				if x != None : result += "23" + x.text  			#track 2
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track3" + xmlns + "Byte")
				if x != None : result += "24" + x.text  			#track 3

			if root.attrib['RequestType'] == 'CardSwipe':
				result = "06C0" 				#tag
				result += "490978" 			#cc

			if root.attrib['RequestType'] == 'LoyaltySwipe':
				result = "06C0" 				#tag
				result += "490978" 			#cc
				result += "0604"				#tlv container
				result += "1F68"				#loyalty tag
				result += "0101"				#loyalty data
			
			if root.attrib['RequestType'] == 'LoyaltySwipe':
				result = "0601" 				#tag
				result += "490978" 			#cc
				result += "0604"				#tlv container
				result += "1F68"				#loyalty tag
				result += "0101"				#loyalty data

			if root.attrib['RequestType'] == 'CardPaymentLoyaltyAward':
				result = "0601" 				#tag
				result += "490978" 			#cc
				x = root.find("." + xmlns + "TotalAmount")
				if x != None : 
					x = hex(int(x.text))[2:]
					result += "04" + x 			#amount
				result += "1902" 				#payment type
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track1" + xmlns + "Byte")
				if x != None : result += "2D" + x.text				#track 1
				x = root.find("." + xmlns + "CardValue" + xmlns + "ExpiryDate")
				if x != None : result += "0E" + x.text 			#expiry date
				x = root.find("." + xmlns + "CardValue" + xmlns + "CardPAN")
				if x != None : result += "22" + x.text			 	#card number
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track2" + xmlns + "Byte")
				if x != None : result += "23" + x.text  			#track 2
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track3" + xmlns + "Byte")
				if x != None : result += "24" + x.text  			#track 3
				result += "0604"				#tlv container
				result += "1F68"				#loyalty tag
				result += "0101"				#loyalty data

			if root.attrib['RequestType'] == 'LoyaltyAward':
				result = "0601" 				#tag
				result += "490978" 			#cc
				x = root.find("." + xmlns + "TotalAmount")
				x = hex(int(x.text))[2:]
				result += "04" + x 			#amount
				result += "1902" 				#payment type
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track1" + xmlns + "Byte")
				if x != None : result += "2D" + x.text				#track 1
				x = root.find("." + xmlns + "CardValue" + xmlns + "ExpiryDate")
				if x != None : result += "0E" + x.text 			#expiry date
				x = root.find("." + xmlns + "CardValue" + xmlns + "CardPAN")
				if x != None : result += "22" + x.text			 	#card number
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track2" + xmlns + "Byte")
				if x != None : result += "23" + x.text  			#track 2
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track3" + xmlns + "Byte")
				if x != None : result += "24" + x.text  			#track 3
				result += "0604"				#tlv container
				result += "1F68"				#loyalty tag
				result += "0101"				#loyalty data

			if root.attrib['RequestType'] == 'CardPreAuthorisation':
				result = "0622" 				#tag
				result += "490978" 			#cc
				result += "1902" 				#payment type
				x = root.find("." + xmlns + "CardValue" + xmlns + "ExpiryDate")
				if x != None : result += "0E" + x.text 			#expiry date
				x = root.find("." + xmlns + "CardValue" + xmlns + "CardPAN")
				if x != None : result += "22" + x.text			 	#card number
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track1" + xmlns + "Byte")
				if x != None : result += "2D" + x.text				#track 1
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track2" + xmlns + "Byte")
				if x != None : result += "23" + x.text  			#track 2
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track3" + xmlns + "Byte")
				if x != None : result += "24" + x.text  			#track 3
			
			if root.attrib['RequestType'] == 'CardFinancialAdvice':
				result = "0623" 				#tag
				result += "490978" 			#cc
				x = root.find("." + xmlns + "OriginalTransaction")
				if x != None : result += "87" + x.text 			#receipt number
				x = root.find("." + xmlns + "TotalAmount")
				x = hex(int(x.text))[2:]
				result += "04" + x 			#amount
				result += "1902" 				#payment type

			if root.attrib['RequestType'] == 'CardPreAuthorisationLoyaltySwipe':
				result = "0622" 				#tag
				result += "490978" 			#cc
				result += "1902" 				#payment type
				x = root.find("." + xmlns + "CardValue" + xmlns + "ExpiryDate")
				if x != None : result += "0E" + x.text 			#expiry date
				x = root.find("." + xmlns + "CardValue" + xmlns + "CardPAN")
				if x != None : result += "22" + x.text			 	#card number
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track1" + xmlns + "Byte")
				if x != None : result += "2D" + x.text				#track 1
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track2" + xmlns + "Byte")
				if x != None : result += "23" + x.text  			#track 2
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track3" + xmlns + "Byte")
				if x != None : result += "24" + x.text  			#track 3
				result += "0604"				#tlv container
				result += "1F68"				#loyalty tag
				result += "0101"				#loyalty data

			if root.attrib['RequestType'] == 'CardFinancialAdviceLoyaltyAward':
				result = "0624" 				#tag
				result += "490978" 			#cc
				x = root.find("." + xmlns + "OriginalTransaction")
				if x != None : result += "87" + x.text 			#receipt number
				x = root.find("." + xmlns + "TotalAmount")
				x = hex(int(x.text))[2:]
				result += "04" + x 			#amount
				result += "1902" 				#payment type
				result += "0604"				#tlv container
				result += "1F68"				#loyalty tag
				result += "0101"				#loyalty data

			if root.attrib['RequestType'] == 'PaymentReversal':
				result = "0630" 				#tag
				result += "000000"			#password
				x = root.find("." + xmlns + "OriginalTransaction")
				result += "87" + x.text 	#receipt number
				result += "490978" 			#cc
				x = root.find("." + xmlns + "TotalAmount")
				if x != None : 
					x = hex(int(x.text))[2:]
					result += "04" + x 			#amount
				result += "1902" 				#payment type
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track1" + xmlns + "Byte")
				if x != None : result += "2D" + x.text				#track 1
				x = root.find("." + xmlns + "CardValue" + xmlns + "ExpiryDate")
				if x != None : result += "0E" + x.text 			#expiry date
				x = root.find("." + xmlns + "CardValue" + xmlns + "CardPAN")
				if x != None : result += "22" + x.text			 	#card number
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track2" + xmlns + "Byte")
				if x != None : result += "23" + x.text  			#track 2
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track3" + xmlns + "Byte")
				if x != None : result += "24" + x.text  			#track 3

			if root.attrib['RequestType'] == 'PaymentLoyaltyReversal':
				result = "0630" 				#tag
				result += "000000"			#password
				x = root.find("." + xmlns + "OriginalTransaction")
				result += "87" + x.text 	#receipt number
				result += "490978" 			#cc
				x = root.find("." + xmlns + "TotalAmount")
				if x != None : 
					x = hex(int(x.text))[2:]
					result += "04" + x 			#amount
				result += "1902" 				#payment type
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track1" + xmlns + "Byte")
				if x != None : result += "2D" + x.text				#track 1
				x = root.find("." + xmlns + "CardValue" + xmlns + "ExpiryDate")
				if x != None : result += "0E" + x.text 			#expiry date
				x = root.find("." + xmlns + "CardValue" + xmlns + "CardPAN")
				if x != None : result += "22" + x.text			 	#card number
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track2" + xmlns + "Byte")
				if x != None : result += "23" + x.text  			#track 2
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track3" + xmlns + "Byte")
				if x != None : result += "24" + x.text  			#track 3
				result += "0604"				#tlv container
				result += "1F68"				#loyalty tag
				result += "0101"				#loyalty data
				
			if root.attrib['RequestType'] == 'PaymentRefund':
				result = "0631" 				#tag
				result += "000000"			#password
				x = root.find("." + xmlns + "TotalAmount")
				x = hex(int(x.text))[2:]
				result += "04" + x 			#amount

			if root.attrib['RequestType'] == 'PaymentLoyaltyRefund':
				result = "0631" 				#tag
				result += "000000"			#password
				x = root.find("." + xmlns + "TotalAmount")
				x = hex(int(x.text))[2:]
				result += "04" + x 			#amount
				result += "0604"				#tlv container
				result += "1F68"				#loyalty tag
				result += "0101"				#loyalty data

			if root.attrib['RequestType'] == 'LoyaltyAwardReversal':
				result = "0630" 				#tag
				result += "000000"			#password
				x = root.find("." + xmlns + "OriginalTransaction")
				result += "87" + x.text 	#receipt number
				result += "490978" 			#cc
				x = root.find("." + xmlns + "TotalAmount")
				if x != None : 
					x = hex(int(x.text))[2:]
					result += "04" + x 			#amount
				result += "1902" 				#payment type
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track1" + xmlns + "Byte")
				if x != None : result += "2D" + x.text				#track 1
				x = root.find("." + xmlns + "CardValue" + xmlns + "ExpiryDate")
				if x != None : result += "0E" + x.text 			#expiry date
				x = root.find("." + xmlns + "CardValue" + xmlns + "CardPAN")
				if x != None : result += "22" + x.text			 	#card number
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track2" + xmlns + "Byte")
				if x != None : result += "23" + x.text  			#track 2
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track3" + xmlns + "Byte")
				if x != None : result += "24" + x.text  			#track 3
				result += "0604"				#tlv container
				result += "1F68"				#loyalty tag
				result += "0101"				#loyalty data

			if root.attrib['RequestType'] == 'LoyaltyRedemptionReversal':
				result = "0630" 				#tag
				result += "000000"			#password
				x = root.find("." + xmlns + "OriginalTransaction")
				result += "87" + x.text 	#receipt number
				result += "490978" 			#cc
				x = root.find("." + xmlns + "TotalAmount")
				if x != None : 
					x = hex(int(x.text))[2:]
					result += "04" + x 			#amount
				result += "1902" 				#payment type
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track1" + xmlns + "Byte")
				if x != None : result += "2D" + x.text				#track 1
				x = root.find("." + xmlns + "CardValue" + xmlns + "ExpiryDate")
				if x != None : result += "0E" + x.text 			#expiry date
				x = root.find("." + xmlns + "CardValue" + xmlns + "CardPAN")
				if x != None : result += "22" + x.text			 	#card number
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track2" + xmlns + "Byte")
				if x != None : result += "23" + x.text  			#track 2
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track3" + xmlns + "Byte")
				if x != None : result += "24" + x.text  			#track 3
				result += "0604"				#tlv container
				result += "1F68"				#loyalty tag
				result += "0101"				#loyalty data

			if root.attrib['RequestType'] == 'CardActivate':
				result = "0604" 				#tag
				result += "490978" 			#cc
				x = root.find("." + xmlns + "CardValue" + xmlns + "ExpiryDate")
				if x != None : result += "0E" + x.text 			#expiry date
				x = root.find("." + xmlns + "CardValue" + xmlns + "CardPAN")
				if x != None : result += "22" + x.text			 	#card number
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track1" + xmlns + "Byte")
				if x != None : result += "2D" + x.text				#track 1
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track2" + xmlns + "Byte")
				if x != None : result += "23" + x.text  			#track 2
				x = root.find("." + xmlns + "CardValue" + xmlns + "Track3" + xmlns + "Byte")
				if x != None : result += "24" + x.text  			#track 3
	
		length = hex((len(result)-4)//2)[2:]
		if len(length) == 1:
			length = '0' + length
		result = length.join([result[:4],result[4:]])

		return(self.spacer(result))

	def spacer(self,string):
		i = 4
		while i < len(string):
			string = string[:i]+" "+string[i:]
			i = i+5
		return(string)	