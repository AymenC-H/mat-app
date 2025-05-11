from PyQt5.QtWidgets import QMessageBox,QTableWidgetItem,QApplication,QWidget,QAbstractItemView
from PyQt5.QtCore import Qt
from app_mat_ui import Ui_Form
from numpy import array,delete,unique,prod,array_equal,zeros,expand_dims,hstack
from fractions import Fraction
from pickle import load,dump
from math import lcm

try:
    fb=open("data_mat.dat",'rb')
    MatS=load(fb)
    fb.close()
except:
    fb=open("data_mat.dat",'wb')
    MatS=[]
    fb.close()
    
class base(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("App_Mat")
        #self.setMinimumWidth(1440)
        #self.setMinimumHeight(840)
        self.refresh_mat()
        self.prod_widget.hide()
        self.sys.hide()
        self.choice()
        self.saisie_mat()
        self.choix.currentIndexChanged.connect(self.choice)
        self.choix.currentIndexChanged.connect(self.saisie_mat)
        self.lm1.valueChanged.connect(self.saisie_mat)
        self.cm2.valueChanged.connect(self.saisie_mat)
        self.lc.valueChanged.connect(self.saisie_mat)
        self.deg.valueChanged.connect(self.saisie_mat)
        self.res.clicked.connect(self.resultat)
        self.save.clicked.connect(self.sauvegarder)
        self.remplir_b.clicked.connect(self.remplir)
        self.supp.clicked.connect(self.supprimer)
    def to_int(self,v:float):
        if int(v)==v:
            return(str(int(v)))
        return(f"{v:3f}")
    def message(self,ch:str):
        message=QMessageBox()
        style=QWidget()
        style.setStyleSheet("background-color:rgb(250,170,177);")
        message.critical(style,"Erreur",ch)
    def choice(self):
        global choix
        choix=self.choix.currentIndex()
        self.save_res.show()
        self.save_res.setEnabled(True)
        self.dim_prod.hide()
        self.dim_prod.setEnabled(False)
        self.sys.hide()
        self.sys.setEnabled(False)
        self.res_det.hide()
        self.res_det.setEnabled(False)
        self.l_et_c.show()
        self.l_et_c.setEnabled(True)
        self.prod_widget.hide()
        self.prod_widget.setEnabled(False)
        self.tab_op_widget.show()
        self.tab_op_widget.setEnabled(True)
        if choix==1:
            self.l_et_c.hide()
            self.l_et_c.setEnabled(False)
            self.sys.show()
            self.sys.setEnabled(True)
        elif choix==2:
            self.save_res.hide()
            self.save_res.setEnabled(False)
            self.res_det.show()
            self.res_det.setEnabled(True)
        elif choix==3:
            self.label_lc_5.setText("Nombre de Lignes M1:")
            self.label_lc_6.setText("Nombre de Colonnes M2:")
            self.prod_widget.show()
            self.prod_widget.setEnabled(True)
            self.tab_op_widget.hide()
            self.tab_op_widget.setEnabled(False)
            self.dim_prod.show()
            self.dim_prod.setEnabled(True)
        elif choix in range(4,7):
            self.label_lc_6.setText("Nombre de Colonnes:")
            self.label_lc_5.setText("Nombre de Lignes:")
            self.dim_prod.show()
            self.dim_prod.setEnabled(True)
            self.l_et_c.hide()
            self.l_et_c.setEnabled(False)
            self.prod_widget.show()
            self.prod_widget.setEnabled(True)
            if choix==6:
                self.tab_op.show()
                self.tab_op.setEnabled(True)
                self.prod_widget.hide()
                self.prod_widget.setEnabled(False)
            else:
                self.tab_op_widget.hide()
                self.tab_op_widget.setEnabled(False)

    def saisie_mat(self):
        #f.sm.setEnabled(False)
        self.tab_res.show()
        self.tab_op.clear()
        self.tab_res.clear()
        self.tab_prod1.clear()
        self.tab_prod2.clear()
        if choix in (0,2) or choix==7:
            N=int(self.lc.value())
            self.tab_op.setRowCount(N)
            self.tab_op.setColumnCount(N)
            self.tab_res.setRowCount(N)
            self.tab_res.setColumnCount(N)
            for L in range(N):
                for C in range(N):
                    self.tab_op.setItem(L,C,QTableWidgetItem(''))
                    self.tab_res.setItem(L,C,QTableWidgetItem(''))
            if choix==2:
                self.tab_res.hide()
                self.res_det.show()
                self.res_det.setEnabled(True)
        elif choix==1:
            N=int(self.deg.value())
            self.tab_op.setRowCount(N)
            self.tab_op.setColumnCount(N+1)
            for L in range(N):
                for C in range(N+1):
                    if L==0:
                        if C!=N:
                            header_item = QTableWidgetItem(f"Coef {C+1}")
                            self.tab_op.setHorizontalHeaderItem(C, header_item)
                        else:
                            header_item = QTableWidgetItem("Resultat")
                            self.tab_op.setHorizontalHeaderItem(N, header_item)             
                    self.tab_op.setItem(L,C,QTableWidgetItem(''))
            self.tab_res.setRowCount(1)
            self.tab_res.setColumnCount(N)
            for C in range(N):
                self.tab_res.setItem(L,C,QTableWidgetItem(''))
        elif choix==3:
            N=int(self.lc.value())
            N1=int(self.lm1.value())
            P2=int(self.cm2.value())
            self.tab_prod1.setRowCount(N1)
            self.tab_prod1.setColumnCount(N)
            self.tab_prod2.setRowCount(N)
            self.tab_prod2.setColumnCount(P2)
            self.tab_res.setRowCount(N1)
            self.tab_res.setColumnCount(P2)
            for L in range(N1):
                for C in range(N):
                    self.tab_prod1.setItem(L,C,QTableWidgetItem(''))
            for L in range(N):
                for C in range(P2):
                    self.tab_prod2.setItem(L,C,QTableWidgetItem(''))
            for L in range(N1):
                for C in range(P2):
                    self.tab_res.setItem(L,C,QTableWidgetItem(''))
        elif choix in range(4,6):
            N=int(self.lm1.value())
            P=int(self.cm2.value())
            self.tab_prod1.setRowCount(N)
            self.tab_prod1.setColumnCount(P)
            self.tab_prod2.setRowCount(N)
            self.tab_prod2.setColumnCount(P)
            self.tab_res.setRowCount(N)
            self.tab_res.setColumnCount(P)
            for L in range(N):
                for C in range(P):
                    self.tab_prod1.setItem(L,C,QTableWidgetItem(''))
            for L in range(N):
                for C in range(P):
                    self.tab_prod2.setItem(L,C,QTableWidgetItem(''))
            for L in range(N):
                for C in range(P):
                    self.tab_res.setItem(L,C,QTableWidgetItem(''))
        elif choix==6:
            N=int(self.lm1.value())
            P=int(self.cm2.value())
            self.tab_op.setRowCount(N)
            self.tab_op.setColumnCount(P)
            self.tab_res.setRowCount(P)
            self.tab_res.setColumnCount(N)
            for L in range(N):
                for C in range(P):
                    self.tab_op.setItem(L,C,QTableWidgetItem(''))
                    self.tab_res.setItem(C,L,QTableWidgetItem(''))
                    self.tab_res.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def produit_mat(self,M1,M2,p,n,pn):
        MR=array([[float()]*p]*n)
        for L in range (n):
            for C in range (p):
                m=0
                for i in range (pn):
                    m=m+M1[L,i]*M2[i,C]
                MR[L,C]=m
        return(MR)

    def pivot_gauss_sys(self,M,L,N,P,c1,c2):
        for C in range(P):
            M[L,C]=M[L,C]*c2-M[L-1,C]*c1
        if self.verif_double_L(M,N):
            return M,1
        return(M,2)

    def produit(self,T,M,l,n):
        pr=0
        for i in range (l,n):
            pr=pr+T[i]*M[l-1,i]
        return(pr)

    def transfert(self,M1,M2,N,P):
        for l in range (N):
            for c in range(N):
                M2[l,c]=M1[l,c]
        return(M2)

    def calc_coef(self,a,b):
        a=int(a);b=int(b)
        if a==0 or b==0:
            return(0,0)
        elif (a>0 and b>0) or (b<0 and a<0):
            lc=lcm(a,b)
            return(lc//a,lc//b)
        else:#(a>0 and b<0) or (b>0 and a<0)
            lc=-lcm(a,b)
            return(lc//a,lc//b)

    def calcul(self,v1,v2,v3,v4):
        return(v1*v4-v2*v3)

    def verif_double_L(self,M,N):
        M2=unique(M,axis=0)
        nb=M2.shape[0]
        for i in range (N):
            if array_equal(M[i],[[0]*(N+1)]):
                return True
        if nb<N:
            return True
        return False

    def system_pivot_gauss(self,M,N):
        if self.verif_double_L(M,N):
            return [0],1
        P=N+1
        minL=1
        while minL<N:
            C=minL-1
            for L in range (N-1,C,-1):
                Lp=M[L-1,C]
                La=M[L,C]
                coefLp,coefLa=self.calc_coef(Lp,La)
                M,b=self.pivot_gauss_sys(M,L,N,P,coefLp,coefLa)
                if b!=2:
                    return [0],1
            minL+=1
        if b!=2:
            return([[0]*N],b)
        S=array([float()]*N)
        S[N-1]=M[N-1,P-1]/M[N-1,P-2]
        for i in range (N-2,-1,-1):
            S[i]=(M[i,P-1]-self.produit(S,M,i+1,N))/M[i,i]
        for i in range(N):
            if sum([a * b for a, b in zip(M[i][:-1],S)])!=M[i][-1]:
                return S,0
        return(S,2)

    def calcul_det(self,M,N):
        if N==2:
            return(self.calcul(M[0,0],M[0,1],M[1,0],M[1,1]))
        else:
            f=-1
            res=0
            for i in range(N):
                f=-f
                MP=array([[float()]*(N-1)]*(N-1))
                lp=0
                for l in range(N):
                    if l==i:
                        continue
                    for c in range(1,N):
                        MP[lp,c-1]=M[l,c]
                    lp=lp+1
                res=res+f*M[i,0]*self.calcul_det(MP,N-1)
            return(res)

    def mat_inverse_gauss(self,M,N):
        S=array([float()]*N)
        MR=array([[float()]*N]*N)
        for l in range(N):
            MS=M.copy()
            T=zeros(3)
            T[l]=1
            MS=hstack((MS,expand_dims(T,axis=1)))
            S,b=self.system_pivot_gauss(MS,N)
            for L in range(N):
                MR[L,l]=S[L]
        return(MR)

    def isfloat(self,num):
        try:
            num=float(eval(num))
            return True,num
        except:
            return False,0

    def resultat(self):
        self.setCursor(Qt.CursorShape.WaitCursor)
        if choix in [4,5]:
            N=self.tab_prod1.rowCount()
            P=self.tab_prod1.columnCount()
            MF=array([[float()]*P]*N)
            MF2=array([[float()]*P]*N)
            for L in range(N):
                for C in range(P):
                    value=self.tab_prod1.item(L,C).text()
                    value2=self.tab_prod2.item(L,C).text()
                    b1,value=self.isfloat(value)
                    b2,value2=self.isfloat(value2)
                    if b1 and b2:
                        MF[L,C]=value
                        MF2[L,C]=value2
                    else:
                        self.message(f"M[{L+1},{C+1}] doit être un nombre réel")
                        self.setCursor(Qt.CursorShape.ArrowCursor)
                        return(0)
            if choix==4:
                for L in range(N):
                    for C in range(P):
                        v=self.to_int(MF[L,C]+MF2[L,C])
                        self.tab_res.setItem(L,C,QTableWidgetItem(v))
            elif choix==5:
                for L in range(N):
                    for C in range(P):
                        v=self.to_int(MF[L,C]-MF2[L,C])
                        self.tab_res.setItem(L,C,QTableWidgetItem(v))
        elif choix==2 or choix==0:
            n=self.tab_op.rowCount()
            MF=array([[float()]*n]*n)
            for L in range(n):
                for C in range(n):
                    value=self.tab_op.item(L,C).text()
                    b,value=self.isfloat(value)
                    if b:
                        MF[L,C]=value
                    else:
                        self.message(f"M[{L+1},{C+1}] doit être un nombre réel")
                        self.setCursor(Qt.CursorShape.ArrowCursor)
                        return(0)
            if choix==2:
                if n==1:
                    self.res_det.setText(str(MF[0,0]))
                else:
                    self.res_det.setText(str(self.calcul_det(MF,n)))
            elif choix==0:
                if self.calcul_det(MF,n)!=0:
                    MI=self.mat_inverse_gauss(MF,n)
                    for L in range(n):
                        for C in range(n):
                            self.tab_res.setItem(L,C,QTableWidgetItem(str(Fraction(MI[L,C]).limit_denominator())))
                else:
                    self.message("Catte matrice n'est pas inversible!")

        elif choix==3:
            n=self.tab_prod1.rowCount()
            p=self.tab_prod2.columnCount()
            pn=self.tab_prod1.columnCount()
            MF=array([[float()]*pn]*n)
            MF2=array([[float()]*p]*pn)
            for L in range(n):
                for C in range(pn):
                    value=self.tab_prod1.item(L,C).text()
                    b,value=self.isfloat(value)
                    if b:
                        MF[L,C]=value
                    else:
                        self.message(f"M[{L+1},{C+1}] doit être un nombre réel")
                        self.setCursor(Qt.CursorShape.ArrowCursor)
                        return(0)
            for L in range(pn):
                for C in range(p):
                    value2=self.tab_prod2.item(L,C).text()
                    b,value2=self.isfloat(value2)
                    if b:
                        MF2[L,C]=value2
                    else:
                        self.message(f"M[{L+1},{C+1}] doit être un nombre réel")
                        return(0)
            MI=self.produit_mat(MF,MF2,p,n,pn)
            for L in range(n):
                for C in range(p):
                    self.tab_res.setItem(L,C,QTableWidgetItem(str(Fraction(MI[L,C]).limit_denominator())))
        elif choix==0:
            n=self.tab_op.rowCount()
            MF=array([[float()]*n]*n)
            for L in range(n):
                for C in range(n):
                    value=self.tab_op.item(L,C).text()
                    b,value=self.isfloat(value)
                    if b:
                        MF[L,C]=value
                    else:
                        self.message(f"M[{L+1},{C+1}] doit être un nombre réel")
                        self.setCursor(Qt.CursorShape.ArrowCursor)
                        return(0)
        elif choix==1:
            n=self.tab_op.rowCount()
            MF=array([[float()]*(n+1)]*n)
            for L in range(n):
                for C in range(n+1):
                    value=self.tab_op.item(L,C).text()
                    b,value=self.isfloat(value)
                    if b:
                        MF[L,C]=value
                    else:
                        self.message(f"M[{L+1},{C+1}] doit être un nombre réel")
                        self.setCursor(Qt.CursorShape.ArrowCursor)
                        return(0)
            T,b=self.system_pivot_gauss(MF,n)
            if b==0:
                style=QWidget()
                style.setStyleSheet("background-color:rgba(0, 190, 140, 70);")
                QMessageBox.information(style,"Impossible","Le système n'a aucune solution!")
            elif b==1:
                style=QWidget()
                style.setStyleSheet("background-color:rgba(0, 190, 140, 70);")
                QMessageBox.information(style,"Impossible","Le système a une infinité de solution!")
            else:
                for L in range(n):
                    self.tab_res.setItem(0,L,QTableWidgetItem(str(Fraction(T[L]).limit_denominator())))
        elif choix==6:
            N=self.tab_op.rowCount()
            P=self.tab_op.columnCount()
            for L in range(N):
                for C in range(P):
                    value=self.tab_op.item(L,C).text()
                    b,value=self.isfloat(value)
                    if b:
                        value=self.to_int(value)
                        self.tab_res.setItem(C,L,QTableWidgetItem(value))
                    else:
                        self.message(f"M[{L+1},{C+1}] doit être un nombre réel")
                        self.setCursor(Qt.CursorShape.ArrowCursor)
                        return(0)
        elif choix==7:
            N=self.tab_op.rowCount()
            MC=array([[float()]*N]*N)
            for L in range(N):
                for C in range(N):
                    value=self.tab_op.item(L,C).text()
                    b,value=self.isfloat(value)
                    if b:
                        MC[L,C]=self.to_int(value)
                    else:
                        self.message(f"M[{L+1},{C+1}] doit être un nombre réel")
                        self.setCursor(Qt.CursorShape.ArrowCursor)
                        return(0)
            for L in range(N):
                MP=delete(MC,L,axis=0)
                for C in range(N):
                    MD=delete(MP,C,axis=1)
                    self.tab_res.setItem(L,C,QTableWidgetItem(self.to_int(self.calcul_det(MD,N-1))))
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def refresh_data(self):
        global MatS
        fb=open("data_mat.dat",'wb')
        dump(MatS,fb)
        fb.close()

    def sauvegarde(self,M):
        global MatS
        N=M.rowCount()
        P=M.columnCount()
        Mat=array([[float]*P]*N)
        for L in range(N):
            for C in range(P):
                value=M.item(L,C).text()
                b,value=self.isfloat(value)
                if b:
                    Mat[L,C]=value
                else:
                    self.message(f"M[{L+1},{C+1}] doit être un nombre réel")
                    return(0)
        Mat=Mat.tolist()
        b,i=False,0
        l=len(MatS)
        while not(b) and i<l:
            b=MatS[i]['Matrice']==Mat
            i+=1
        if b:
            self.message("Cette matrice existe déjà!")
            return 0
        MatS.append({'Rang':l+1,"Matrice":Mat,'Lignes':N,'Colonnes':P})
        self.Mat_S.addItem('Matrice '+str(l+1)+' ('+str(N)+','+str(P)+')')
        self.refresh_data()

    def refresh_data(self):
        global MatS
        fb=open("data_mat.dat",'wb')
        dump(MatS,fb)
        fb.close()
    def sauvegarde(self,M):
        global MatS
        N=M.rowCount()
        P=M.columnCount()
        Mat=array([[float]*P]*N)
        for L in range(N):
            for C in range(P):
                value=M.item(L,C).text()
                b,value=self.isfloat(value)
                if b:
                    Mat[L,C]=value
                else:
                    self.message(f"M[{L+1},{C+1}] doit être un nombre réel")
                    return(0)
        Mat=Mat.tolist()
        b,i=False,0
        l=len(MatS)
        while not(b) and i<l:
            b=MatS[i]['Matrice']==Mat
            i+=1
        if b:
            self.message(f"Cette matrice existe déjà ({i})!")
            return 0
        MatS.append({'Rang':l+1,"Matrice":Mat,'Lignes':N,'Colonnes':P})
        self.Mat_S.addItem('Matrice '+str(l+1)+' ('+str(N)+','+str(P)+')')
        self.refresh_data()
    
    def sauvegarder(self):
        nb=self.choix.currentIndex()
        b=True
        if self.save_res.isChecked() and nb!=2:
            self.sauvegarde(self.tab_res)
            b=False
        if nb in range(3,6):
            if self.save_m1.isChecked():
                self.sauvegarde(self.tab_prod1)
                b=False
            if self.save_m2.isChecked():
                self.sauvegarde(self.tab_prod2)
                b=False
        if self.save_op.isChecked() and not(nb in range(3,6)):
            self.sauvegarde(self.tab_op)
            b=False
        if b:
            self.message("Veuillez sélectionner au moins une matrice à sauvegarder!")
            return 0
        
    def remplir_mat(self, M):
        global MatS
        rang=self.Mat_S.currentIndex()
        Mat=MatS[rang]["Matrice"]
        P,N=MatS[rang]['Colonnes'],MatS[rang]['Lignes']
        P2,N2=M.columnCount(),M.rowCount()
        P,N=min(P,P2),min(N,N2)
        for l in range(N):
            for c in range(P):
                v=self.to_int(Mat[l][c])
                M.setItem(l,c,QTableWidgetItem(v))
                M.setItem(l,c,QTableWidgetItem(v))

    def remplir(self):
        nb=self.choix.currentIndex()
        b=True
        if self.Mat_S.count()==0:
            self.message("Il n'y a pas de matrices sauvegardés")
            return(0)
        if self.save_op.isChecked() and not(nb in range(3,6)):
            self.remplir_mat(self.tab_op)
            b=False
        if nb in range(3,6):
            if self.save_m1.isChecked():
                self.remplir_mat(self.tab_prod1)
                b=False
            if self.save_m2.isChecked():
                self.remplir_mat(self.tab_prod2)
                b=False
        if b:
            self.message("Veuillez sélectionner au moins une matrice à remplir!")
            return 0
        

    def refresh_mat(self):
        self.Mat_S.clear()
        l=len(MatS)
        for i in range (l):
            aux=MatS[i]
            self.Mat_S.addItem('Matrice '+str(aux['Rang'])+' ('+str(aux['Lignes'])+','+str(aux['Colonnes'])+')')

    def supprimer(self):
        global MatS
        if self.Mat_S.count()==0:
            self.message("Il n'y a pas de matrices sauvegardées")
            return(0)
        rang=self.Mat_S.currentIndex()
        MatS.pop(rang)
        l=len(MatS)
        for i in range(rang,l):
            MatS[i]['Rang']-=1
        self.refresh_mat()
        self.refresh_data()

