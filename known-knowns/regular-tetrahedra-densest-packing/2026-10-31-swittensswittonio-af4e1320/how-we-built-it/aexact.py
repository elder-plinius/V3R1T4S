from mpmath import mp, mpf, sqrt, acos, asin, pi, sin, cos, matrix
mp.dps=30
th=acos(mpf(1)/3)
def a_exact(r):
    r=mpf(r); h=r*sin(th/2)
    if r>=1: return mpf(0)
    n1=(sin(th/2),0,-cos(th/2)); n2=(sin(th/2),0,cos(th/2))
    p=(r,sqrt(1-r*r),0)
    # check n_i.p=h
    g=lambda n:[n[i]-h*p[i] for i in range(3)]
    g1,g2=g(n1),g(n2)
    dot=sum(x*y for x,y in zip(g1,g2)); 
    ang=acos(dot/(sqrt(sum(x*x for x in g1))*sqrt(sum(x*x for x in g2))))
    phi=pi-ang
    psi=2*asin(sqrt(1-r*r)/sqrt(1-h*h))
    return (2*phi-2*h*psi)/(4*pi)
if __name__=="__main__":
    al=th/(2*pi)
    ref={0:0.19595,0.05:.18163,0.1:.16780,0.2:.14120,0.4:.09273,0.6:.05125,0.8:.01849}
    for r,v in ref.items():
        t=al-r/(2*sqrt(3))+sqrt(2)/18*r*r
        print(r,"exact",mp.nstr(a_exact(r),6),"grid",v,"taylor",mp.nstr(t,6))
