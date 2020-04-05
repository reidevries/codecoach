import bibtex
import unittest
class TestAuthorExtract(unittest.TestCase):
	def setUp(self):
		self.simple_author_1 = "Smith"
		self.simple_author_2 = "Jones"
		self.author_1 = "John Smith"
		self.author_2 = "Bob Jones"
		self.author_3 = "Justin Kenneth Pearson"
		self.surname_first_1 = "Pearson, Justin Kenneth"
		self.surname_first_2 = "Van Hentenryck, Pascal"
		self.multiple_authors_1 = "Pearson, Justin and Jones, Bob"
		
	def test_author_1(self):
		(Surname,FirstNames) = bibtex.extract_author(self.simple_author_1)
		self.assertEqual((Surname,FirstNames),("Smith",""))
		(Surname,FirstNames) = bibtex.extract_author(self.simple_author_2)
		self.assertEqual( (Surname,FirstNames) , ("Jones","") )
	
	
	def test_author_2(self):
		(Surname,FirstNames) = bibtex.extract_author(self.author_1)
		self.assertEqual((Surname,FirstNames),("Smith","John"))
		(Surname,FirstNames) = bibtex.extract_author(self.author_2)
		self.assertEqual( (Surname,FirstNames) , ("Jones","Bob") )

	def test_author_3(self):
		(Surname,FirstNames) = bibtex.extract_author(self.author_3)
		self.assertEqual((Surname,FirstNames),("Pearson","Justin Kenneth"))

	def test_surname_first(self):
		(Surname,FirstNames) = bibtex.extract_author(self.surname_first_1)
		self.assertEqual((Surname,FirstNames),("Pearson","Justin Kenneth"))
		(Surname,FirstNames) = bibtex.extract_author(self.surname_first_2)
		self.assertEqual((Surname,FirstNames),("Van Hentenryck","Pascal"))
 
	
	def test_multiple_author(self):
		Authors = bibtex.extract_authors(self.multiple_authors_1)
		self.assertEqual(Authors[0],("Pearson","Justin"))
		self.assertEqual(Authors[1],("Jones","Bob"))
				
	
if __name__ == '__main__':
	unittest.main()
