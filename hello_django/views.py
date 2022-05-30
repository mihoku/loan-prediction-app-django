from django.shortcuts import render, redirect, get_object_or_404
from .models import ExecutingAgency, Lender, Loan
from .forms import EAForm, LenderForm, LoanForm
from django.views.generic import ListView, DetailView
import pickle
import pathlib
import math


PATH = pathlib.Path(__file__).parent
MODEL_PATH = PATH.joinpath("saved-models").resolve()

#import model 
#model 1 classification numerous drawing limit amendment
model_1_rf = pickle.load(open(MODEL_PATH.joinpath("finalized_model_a.sav"), "rb"))
#model 2 multiclass classification disbursement ratio percentage
model_2_rf = pickle.load(open(MODEL_PATH.joinpath("finalized_model2_a.sav"), "rb"))

# Create your views here.
class EAIndexView(ListView):
    template_name = 'hello_django/ea-index.html'
    context_object_name = 'ea_list'

    def get_queryset(self):
        return ExecutingAgency.objects.all()

class EADetailView(DetailView):
    model = ExecutingAgency
    template_name = 'hello_django/ea-detail.html'

def eaCreate(request):
    if request.method == 'POST':
        form = EAForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ea/index')
    form = EAForm()

    return render(request,'hello_django/ea-create.html',{'form': form})

def eaEdit(request, pk, template_name='hello_django/ea-edit.html'):
    ea = get_object_or_404(ExecutingAgency, pk=pk)
    form = EAForm(request.POST or None, instance=ea)
    if form.is_valid():
        form.save()
        return redirect('ea/index')
    return render(request, template_name, {'form':form})

def eaDelete(request, pk, template_name='hello_django/ea_confirm_delete.html'):
    ea = get_object_or_404(ExecutingAgency, pk=pk)
    if request.method=='POST':
        ea.delete()
        return redirect('ea/index')
    return render(request, template_name, {'object':ea})

#for lender
class lenderIndexView(ListView):
    template_name = 'hello_django/lender-index.html'
    context_object_name = 'lender_list'

    def get_queryset(self):
        return Lender.objects.all()

class lenderDetailView(DetailView):
    model = Lender
    template_name = 'hello_django/lender-detail.html'

def lenderCreate(request):
    if request.method == 'POST':
        form = LenderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lender/index')
    form = LenderForm()

    return render(request,'hello_django/lender-create.html',{'form': form})

def lenderEdit(request, pk, template_name='hello_django/lender-edit.html'):
    lender = get_object_or_404(Lender, pk=pk)
    form = LenderForm(request.POST or None, instance=lender)
    if form.is_valid():
        form.save()
        return redirect('lender/index')
    return render(request, template_name, {'form':form})

def lenderDelete(request, pk, template_name='hello_django/lender_confirm_delete.html'):
    lender = get_object_or_404(Lender, pk=pk)
    if request.method=='POST':
        lender.delete()
        return redirect('lender/index')
    return render(request, template_name, {'object':lender})


LOANTYPE=["Pinjaman Luar Negeri","Pinjaman Dalam Negeri"]

PROGRAMS=["Pembelian Barang","Program Pemerintah","Pembangunan Infrastruktur"]

LENDERTYPE=["Kreditor Swasta Asing (KSA)","Lembaga Penjamin Kredit Ekspor (LPKE)","Lembaga Multilateral","Negara (Bilateral)","Bank BUMN Dalam Negeri","Bank Swasta Dalam Negeri"]

EATYPE=["Kementerian/Lembaga","Badan Usaha Milik Negara","Pemerintah Daerah"]

TARGET1={
    "0":"Numerous Drawing Limit Amendment: False",
    "1": "Numerous Drawing Limit Amendment: True"
    }

TARGET2={
    "0":"Disbursement Under 50%",
    "1":"Disbursement Under 90%",
    "2":"Fully Disbursed"
    }

#for loan
class loanIndexView(ListView):
    template_name = 'hello_django/loan-index.html'
    context_object_name = 'loan_list'

    def get_queryset(self):
        return Loan.objects.all()

class loanDetailView(DetailView):
    model = Loan
    template_name = 'hello_django/loan-detail.html'

def loanCreate(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loan/index')
    form = LoanForm()

    return render(request,'hello_django/loan-create.html',{'form': form})

def loanEdit(request, pk, template_name='hello_django/loan-edit.html'):
    loan = get_object_or_404(Loan, pk=pk)
    form = LoanForm(request.POST or None, instance=loan)
    if form.is_valid():
        form.save()
        return redirect('loan/index')
    return render(request, template_name, {'form':form})

def loanDelete(request, pk, template_name='hello_django/loan_confirm_delete.html'):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method=='POST':
        loan.delete()
        return redirect('loan/index')
    return render(request, template_name, {'object':loan})

def loanPredict(request, pk, template_name='hello_django/loan_prediction_result.html'):
    loan=get_object_or_404(Loan, pk=pk)
    lender = loan.Lender.name
    ea = loan.ExecutingAgency.name
    a = loan.ExecutingAgency.cluster
    b = loan.Lender.cluster
    c = loan.Amount
    d = loan.AvailabilityPeriod
    e = loan.LoanProject.pk
    f = loan.ExecutingAgency.EAType.pk
    g = loan.Lender.LenderType.pk
    h = loan.LoanType.pk
    DisbursementRatioPrediction = predictLoanDisbursementRatio(a,b,c,d,e,f,g,h)
    AmendmentPrediction = predictLoanAmendment(a,b,c,d,e,f,g,h)
    return render(request, template_name, {'LoanTitle':loan.title,'lender':lender,'ea':ea,'DisbursementRatioPrediction':DisbursementRatioPrediction,'AmendmentPrediction':AmendmentPrediction})

#prediction
def predictLoanDisbursementRatio(a,b,c,d,e,f,g,h):
    
    # a adalah cluster EA
    # b adalah cluster Lender
    # c adalah nilai pinjaman
    # d adalah availability period
    # e adalah tipe proyek yang dibiayai pinjaman
    # f adalah tipe executing agency
    # g adalah tipe lender
    # h adalah tipe pinjaman (dalam atau luar negeri)

    eac = a+1    
    lc = b+1
    
    var1 = math.log10(c)
    var2 = 365*d
    var3 = (h==1)
    var4 = (h==2)
    var5 = (e==1)
    var6 = (e==2)
    var7 = (e==3)
    var22 = (f==1)
    var23 = (f==2)
    var8 = (eac==3)
    var9 = (eac==2)
    var10 = (eac==1)
    var11 = (eac==4)
    var12 = (g==1)
    var13 = (g==2)
    var14 = (g==3)
    var15 = (g==4)
    var16 = (g==5)
    var17 = (g==6)
    var18 = (lc==1)
    var19 = (lc==4)
    var20 = (lc==3)
    var21 = (lc==2)    
    
    # pred1 = model_2_vc.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    # pred2 = model_1_vc.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    pred1a = model_2_rf.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    # pred1b = model_2_logreg.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    # pred1c = model_2_knn.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    #pred2a = model_1_rf.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    # pred2b = model_1_logreg.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    # pred2c = model_1_knn.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
        
    recommendation1 = "Pinjaman yang berasal dari lender {} (Cluster {}) senilai Rp {} dengan jangka waktu (availability period) {} tahun, untuk keperluan pembiayaan {} yang dilaksanakan oleh executing agency {} (Cluster {}) {}".format(LENDERTYPE[g-1],lc,c,d,PROGRAMS[e-1],EATYPE[f-1],eac,verdict1(pred1a))
    
    return recommendation1

def predictLoanAmendment(a,b,c,d,e,f,g,h):
    
    # a adalah cluster EA
    # b adalah cluster Lender
    # c adalah nilai pinjaman
    # d adalah availability period
    # e adalah tipe proyek yang dibiayai pinjaman
    # f adalah tipe executing agency
    # g adalah tipe lender
    # h adalah tipe pinjaman (dalam atau luar negeri)

    eac = a+1    
    lc = b+1
    
    var1 = math.log10(c)
    var2 = 365*d
    var3 = (h==1)
    var4 = (h==2)
    var5 = (e==1)
    var6 = (e==2)
    var7 = (e==3)
    var22 = (f==1)
    var23 = (f==2)
    var8 = (eac==3)
    var9 = (eac==2)
    var10 = (eac==1)
    var11 = (eac==4)
    var12 = (g==1)
    var13 = (g==2)
    var14 = (g==3)
    var15 = (g==4)
    var16 = (g==5)
    var17 = (g==6)
    var18 = (lc==1)
    var19 = (lc==4)
    var20 = (lc==3)
    var21 = (lc==2)    
    
    # pred1 = model_2_vc.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    # pred2 = model_1_vc.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    #pred1a = model_2_rf.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    # pred1b = model_2_logreg.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    # pred1c = model_2_knn.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    pred2a = model_1_rf.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    # pred2b = model_1_logreg.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
    # pred2c = model_1_knn.predict([[var1, var2, var3, var4, var5, var6, var7, var22, var23, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21]])
        
    recommendation2 = "Pinjaman yang berasal dari lender {} (Cluster {}) senilai Rp {} dengan jangka waktu (availability period) {} tahun, untuk keperluan pembiayaan {} yang dilaksanakan oleh executing agency {} (Cluster {}) {}".format(LENDERTYPE[g-1],lc,c,d,PROGRAMS[e-1],EATYPE[f-1],eac,verdict2(str(pred2a)))
    
    return recommendation2

def verdict1(pred1):
    if(pred1=="DISBURSEMENT UNDER 50%"):
        return "diprediksikan akan memiliki tingkat pencairan/realisasi yang rendah yakni di bawah 50% dari nilai komitmen"
    elif(pred1=="DISBURSEMENT UNDER 90%"):
        return "diprediksikan akan memiliki tingkat pencairan/realisasi antara 50-90% dari nilai komitmen"
    elif(pred1=="FULLY DISBURSED"):
        return "diprediksikan akan memiliki tingkat pencairan/kinerja realisasi yang baik, yakni di atas 90% nilai komitmen pinjaman dapat direalisasikan"
    else:
        return ""

def verdict2(pred2):
    if(pred2=="[True]"):
        return "diprediksikan akan mengalami lebih dari dua kali amandemen date drawing limit"
    elif(pred2=="[False]"):
        return "diprediksikan tidak akan mengalami lebih dari dua kali amandemen date drawing limit"
    else:
        return ""