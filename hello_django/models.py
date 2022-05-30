from django.db import models

# Create your models here.
class EAType(models.Model):
     classification = models.CharField("Executing Agency Type", max_length=255, blank = True, null = True)  

     def __str__(self):
        return self.classification 

class ExecutingAgency(models.Model):
    name = models.CharField("Executing Agency Name", max_length=255, blank = True, null = True)
    cluster = models.IntegerField()
    EAType = models.ForeignKey(EAType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class LenderType(models.Model):
     classification = models.CharField("Lender Type", max_length=255, blank = True, null = True)

     def __str__(self):
        return self.classification  

class Lender(models.Model):
    name = models.CharField("Lender Name", max_length=255, blank = True, null = True)
    cluster = models.IntegerField()
    LenderType = models.ForeignKey(LenderType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class LoanProject(models.Model):
     classification = models.CharField("Loan Project Type", max_length=255, blank = True, null = True)

     def __str__(self):
        return self.classification 

class LoanType(models.Model):
     classification = models.CharField("Loan Type", max_length=255, blank = True, null = True)

     def __str__(self):
        return self.classification 

class Loan(models.Model):
    title = models.CharField("Loan Name", max_length=455, blank = True, null = True)
    LoanType = models.ForeignKey(LoanType, on_delete=models.CASCADE)
    Lender = models.ForeignKey(Lender, on_delete=models.CASCADE)
    ExecutingAgency = models.ForeignKey(ExecutingAgency, on_delete=models.CASCADE)
    LoanProject = models.ForeignKey(LoanProject, on_delete=models.CASCADE)
    AvailabilityPeriod = models.IntegerField("Availability Period (years)")
    Amount = models.FloatField("Loan Amount (Rp)")

    def __str__(self):
        return self.title