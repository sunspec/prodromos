

/*
 * Include Files
 *
 */
#if defined(MATLAB_MEX_FILE)
#include "tmwtypes.h"
#include "simstruc_types.h"
#else
#include "rtwtypes.h"
#endif

/* %%%-SFUNWIZ_wrapper_includes_Changes_BEGIN --- EDIT HERE TO _END */


#include <math.h>
/* %%%-SFUNWIZ_wrapper_includes_Changes_END --- EDIT HERE TO _BEGIN */
#define u_width 1
#define y_width 1
/*
 * Create external references here.  
 *
 */
/* %%%-SFUNWIZ_wrapper_externs_Changes_BEGIN --- EDIT HERE TO _END */


/* extern double func(double a); */
/* %%%-SFUNWIZ_wrapper_externs_Changes_END --- EDIT HERE TO _BEGIN */

/*
 * Output functions
 *
 */
void ssn_xfosat_cda_Outputs_wrapper(const real_T *x_in,
			const real_T *Vnodal,
			const real_T *R2,
			const real_T *L2,
			const real_T *k,
			const real_T *Lm,
			const real_T *phi0,
			const real_T *backeuler_flag,
			real_T *x_out,
			real_T *Ihist,
			real_T *Y,
			real_T *flux_mag,
			real_T *version,
			const real_T *xD,
			const real_T  *Ts, const int_T  p_width0,
			const real_T  *R1, const int_T  p_width1,
			const real_T  *L1, const int_T  p_width2,
			const real_T  *Rm, const int_T  p_width3)
{
/* %%%-SFUNWIZ_wrapper_Outputs_Changes_BEGIN --- EDIT HERE TO _END */


/* version contains number and date */

/* vector of 'states' that must be used in MdlOutput
 *so they are kept in the x_in x_out loop
 *x_out[0,1,2] partial current states used for current injection
 *x_out[3] time
 */

/* circuit continu
           i1            ix/k          ix           i2
 |---R1----L1->------|--|->-|         |->---L2--R2--<--|
 +                +  |  |   |-|     |-|                +
 V1               Vx Rm Lm    | 1:k | k*Vx             V2   (im is Lm current pointing to the bottom)
 |                   |  |   |-|     |-|                |
 |      |--V3+-------|--|---|         |-------+V4--|   |
 gnd----|------------------------------------------|---|---
 *equation state-space
               d/dt
 [L1  0      1][i1]   [-R1  0         0][i1]   [1 0 -1  0  0]
 [0   L2     k][i2] = [0   -R2        0][i2] + [0 1  0 -1  0]*[v1 v2 v3 v4  phi0]'
 [0    0     1][fm]   [Rm   Rm*k -Rm/Lm][fm]   [0 0  0  0  Rm/Lm]

 [i1 i2 i3 i4]'=[ 1 0 0]*[i1 i2 fm]'
                [ 0 1 0]
                [-1 0 0]
                [0 -1 0]           

 im=fm/Lm-phi0/Lm
 
       fm
       ^              2
       |      1       *   <--- slope between 1-2 is Lsat
 phisat|     *  <---  this is the knee of fm=f(im)
 ~phi0 |
       |   
       |0  <-----slope between 0-1 is Lcore
       *------------------- im
 

 
 step 1: (completion of group state, the inductance current) iL=-I-vnode/Rtot  (From last I and vnode)
 step 2: (update of inductance historty source) : iHL=iL(t-h)+vL(t-h)=2*iL(t-h)-iHL(t-h)
 step 3: (compute new injection for the group: I=-(vs+iHL*RL)/Rtot   (minus sign because of SSN convention)
 **/


real_T  invL[9];
real_T  A[9];
real_T  Ad[9];   // discrete A matrix
real_T  Atmp[9];
real_T  B[15];
real_T  Bd[15];  // discrete B matrix
real_T  IhA2[9];
real_T  ip[3];
real_T il[3]; // inductance state
real_T  inverse_det, tmp, fac;

int i,j,w;

version[0]=3;      // revision start here
version[1]=200815; // date jour mois annee

x_out[3]=x_in[3]+Ts[0]; // time update
if (backeuler_flag[0]<0.5) fac=2; 
else fac=1;

// L inverse found directly
inverse_det=1.0/(L1[0]*L2[0]);  // determinant of upper triangular matrix is the product of diagonal elements

invL[0]=L2[0]*inverse_det;
invL[1]=0;
invL[2]=-L2[0]*inverse_det;
invL[3]=0;
invL[4]=L1[0]*inverse_det;
invL[5]=-L1[0]*k[0]*inverse_det;;
invL[6]=0; 
invL[7]=0;   
invL[8]=L1[0]*L2[0]*inverse_det;


A[0]=0-invL[0]*R1[0]+invL[2]*Rm[0];
A[1]=invL[2]*Rm[0]*k[0];
A[2]=0-invL[2]*Rm[0]/Lm[0];
A[3]=invL[5]*Rm[0];
A[4]=0-invL[4]*R2[0]+invL[5]*Rm[0]*k[0];
A[5]=0-invL[5]*Rm[0]/Lm[0];
A[6]=invL[8]*Rm[0];
A[7]=invL[8]*Rm[0]*k[0];
A[8]=0-invL[8]*Rm[0]/Lm[0];



//Aout[0]=-invL[0]*R1[0]+invL[2]*Rm[0];
//Aout[1]=inverse_det;
//ssPrintf("xxx %e %e %e %e %e\n", A[0], invL[0] , R1[0], invL[2],Rm[0]);

// sotckage de B tranposée
B[0]=invL[0];  B[3]=0;       B[6]=-invL[0];   B[9]=0;
B[1]=0;        B[4]=invL[4]; B[7]=0;          B[10]=-invL[4];
B[2]=0;        B[5]=0;       B[8]=0;          B[11]=0;
// ajout de la colonne phi0
B[12]=invL[2]*Rm[0]/Lm[0];
B[13]=invL[5]*Rm[0]/Lm[0];
B[14]=invL[8]*Rm[0]/Lm[0];

// discretisation Trapezoidal  Ad=inv(I-hA/2)*(I+hA/2)  Bd1=Bd2=inv(I-hA/2)*B*h/2
// I+hA/2  stocké en transposée!
if (backeuler_flag[0]<0.5){
Atmp[0]=1+A[0]*Ts[0]/2;
Atmp[4]=1+A[4]*Ts[0]/2;
Atmp[8]=1+A[8]*Ts[0]/2;
Atmp[3]=A[1]*Ts[0]/2;
Atmp[6]=A[2]*Ts[0]/2;
Atmp[1]=A[3]*Ts[0]/2;
Atmp[7]=A[5]*Ts[0]/2;
Atmp[2]=A[6]*Ts[0]/2;
Atmp[5]=A[7]*Ts[0]/2;
}
else {
Atmp[0]=1;
Atmp[4]=1;
Atmp[8]=1;
Atmp[3]=0;
Atmp[6]=0;
Atmp[1]=0;
Atmp[7]=0;
Atmp[2]=0;
Atmp[5]=0;

}

// I-hA/2 trapeze I-hA backEuler

A[0]=1-A[0]*Ts[0]/fac;
A[4]=1-A[4]*Ts[0]/fac;
A[8]=1-A[8]*Ts[0]/fac;
A[1]=-A[1]*Ts[0]/fac;
A[2]=-A[2]*Ts[0]/fac;
A[3]=-A[3]*Ts[0]/fac;
A[5]=-A[5]*Ts[0]/fac;
A[6]=-A[6]*Ts[0]/fac;
A[7]=-A[7]*Ts[0]/fac;

 
// inverse
inverse_det=1/(A[0]*A[4]*A[8]+ A[1]*A[5]*A[6]+ A[2]*A[3]*A[7]- A[2]*A[4]*A[6]- A[1]*A[3]*A[8]- A[0]*A[5]*A[7]);  // determinant of upper/lower triangular matrix is the product of diagonal elements

IhA2[0]=(A[4]*A[8]-A[5]*A[7])*inverse_det;
IhA2[1]=-(A[1]*A[8]-A[2]*A[7])*inverse_det;
IhA2[2]=(A[1]*A[5]-A[2]*A[4])*inverse_det;
IhA2[3]=-(A[3]*A[8]-A[5]*A[6])*inverse_det;
IhA2[4]=(A[0]*A[8]-A[2]*A[6])*inverse_det;
IhA2[5]=-(A[0]*A[5]-A[2]*A[3])*inverse_det;
IhA2[6]= (A[3]*A[7]-A[4]*A[6])*inverse_det;       // inverse found by adjoint calculation with + - + - alternance
IhA2[7]=-(A[0]*A[7]-A[1]*A[6])*inverse_det;
IhA2[8]=(A[0]*A[4]-A[1]*A[3])*inverse_det;


for (i=0;i<3;i++){
    for (j=0;j<3;j++){
            tmp=0;
        for (w=0;w<3;w++){
            tmp+=IhA2[i*3+w]*Atmp[j*3+w];
        }
        Ad[i*3+j]=tmp;
    }
}

    

for (i=0;i<3;i++){
    for (j=0;j<5;j++){
            tmp=0;
        for (w=0;w<3;w++){
            tmp+=IhA2[i*3+w]*B[j*3+w];
        }
        Bd[i*5+j]=tmp*Ts[0]/fac;
    }
}



// i_out=Y*V_in this is a V-type group  Y=C*Bd2

// nodal admittance of the group
// watch out for column-wize stuff in Simulink.
Y[0]=Bd[0];
Y[4]=Bd[1];
Y[8]=Bd[2];
Y[12]=Bd[3];
Y[1]=Bd[5];
Y[5]=Bd[6];
Y[9]=Bd[7];
Y[13]=Bd[8];
Y[2]=-Bd[0];
Y[6]=-Bd[1];
Y[10]=-Bd[2];
Y[14]=-Bd[3];
Y[3]=-Bd[5];
Y[7]=-Bd[6];
Y[11]=-Bd[7];
Y[15]=-Bd[8];
/*
Y[8]=-Bd[0];
Y[9]=-Bd[1];
Y[10]=-Bd[2];
Y[11]=-Bd[3];
Y[12]=-Bd[4];
Y[13]=-Bd[5];
Y[14]=-Bd[6];
Y[15]=-Bd[7];
 */



// finish the state update from the last nodal solution

ip[0]=Bd[0]*Vnodal[0]+Bd[1]*Vnodal[1]+Bd[2]*Vnodal[2]+ Bd[3]*Vnodal[3];
ip[1]=Bd[5]*Vnodal[0]+Bd[6]*Vnodal[1]+Bd[7]*Vnodal[2] +Bd[8]*Vnodal[3] ;
ip[2]=Bd[10]*Vnodal[0]+Bd[11]*Vnodal[1]+Bd[12]*Vnodal[2]+Bd[13]*Vnodal[3];

il[0]=x_in[0]+ip[0];
il[1]=x_in[1]+ip[1];
il[2]=x_in[2]+ip[2];

flux_mag[0]=il[2];  // flux dans Lm 

// the completion of  old step finish here

// new history source
// injection to the global nodal admitance problem.
// as for normal SSN groups, we consider the current entering the group
// so we must output the negation, current going out of the node
// the SSN YV=I routine summates -Ihist


if (backeuler_flag[0]<0.5){
ip[0]=Ad[0]*il[0]+Ad[1]*il[1]+Ad[2]*il[2]+ip[0]+Bd[4]*phi0[0]*2;  
ip[1]=Ad[3]*il[0]+Ad[4]*il[1]+Ad[5]*il[2]+ip[1]+Bd[9]*phi0[0]*2;
ip[2]=Ad[6]*il[0]+Ad[7]*il[1]+Ad[8]*il[2]+ip[2]+Bd[14]*phi0[0]*2;
}
else {
ip[0]=Ad[0]*il[0]+Ad[1]*il[1]+Ad[2]*il[2]+Bd[4]*phi0[0];  
ip[1]=Ad[3]*il[0]+Ad[4]*il[1]+Ad[5]*il[2]+Bd[9]*phi0[0];
ip[2]=Ad[6]*il[0]+Ad[7]*il[1]+Ad[8]*il[2]+Bd[14]*phi0[0];  
}

Ihist[0]=ip[0];
Ihist[1]=ip[1];
Ihist[2]=-ip[0];
Ihist[3]=-ip[1];   // C*{ Ad*x[n-1]+Bd*u[n-1] }


// keep the value for completion of inductance state calculation
x_out[0]=ip[0];
x_out[1]=ip[1];
x_out[2]=ip[2];
//for (i=0;i<15;i++) x_out[i+4]=Bd[i];
/* %%%-SFUNWIZ_wrapper_Outputs_Changes_END --- EDIT HERE TO _BEGIN */
}

/*
  * Updates function
  *
  */
void ssn_xfosat_cda_Update_wrapper(const real_T *x_in,
			const real_T *Vnodal,
			const real_T *R2,
			const real_T *L2,
			const real_T *k,
			const real_T *Lm,
			const real_T *phi0,
			const real_T *backeuler_flag,
			real_T *x_out,
			real_T *Ihist,
			real_T *Y,
			real_T *flux_mag,
			real_T *version,
			real_T *xD,
			const real_T  *Ts,  const int_T  p_width0,
			const real_T  *R1,  const int_T  p_width1,
			const real_T  *L1,  const int_T  p_width2,
			const real_T  *Rm,  const int_T  p_width3)
{
  /* %%%-SFUNWIZ_wrapper_Update_Changes_BEGIN --- EDIT HERE TO _END */


 
/* %%%-SFUNWIZ_wrapper_Update_Changes_END --- EDIT HERE TO _BEGIN */
}
