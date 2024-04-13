from manim import *

scale_factor = 1

def multivecdefiner(arramp,arrang,arrvecs,arrcirc,ind):
    if ind==0:
        vec = FourierVector(np.array([arramp[ind]/scale_factor,0,0]), buff = 0.0, max_tip_length_to_length_ratio = 0.1, color=WHITE)
        arrcirc.append(Circle(radius = arramp[ind]/scale_factor, stroke_width=0.25, color=WHITE))
        vec.set_angle(arrang[ind])
        arrvecs.append(vec)

        multivecdefiner(arramp,arrang,arrvecs,arrcirc,ind+1)

    elif ind>0 and ind<len(arramp)-1:
        vec = FourierVector(np.array([arramp[ind]/scale_factor,0,0]), buff = 0.0, max_tip_length_to_length_ratio = 0.1, color=WHITE)
        arrcirc.append(Circle(radius = arramp[ind]/scale_factor, stroke_width=0.25, color=WHITE))
        vec.set_angle(arrang[ind])
        arrvecs.append(vec)
        vec.move_to(arrvecs[ind-1].get_end()+ 0.5*arrvecs[ind].get_complete_vector())

        multivecdefiner(arramp,arrang,arrvecs,arrcirc,ind+1)

    else:
        vec = FourierVector(np.array([arramp[ind]/scale_factor,0,0]), buff = 0.0, max_tip_length_to_length_ratio = 0.1, color=WHITE)
        arrcirc.append(Circle(radius = arramp[ind]/scale_factor, stroke_width=0.25, color=WHITE))
        vec.set_angle(arrang[ind])
        arrvecs.append(vec)
        vec.move_to(arrvecs[ind-1].get_end()+ 0.5*arrvecs[ind].get_complete_vector())

def multivecupdater(vecarr,circarr,ind,arrang,arrfreq,tracker):
    if ind > 0:
        vecarr[ind].add_updater(lambda m : m.set_angle(arrang[ind]+arrfreq[ind]*tracker.get_value()))
        vecarr[ind].add_updater(lambda m : m.move_to(vecarr[ind-1].get_end()+ 0.5*vecarr[ind].get_complete_vector()))
        circarr[ind].add_updater(lambda m : m.move_to(vecarr[ind-1].get_end()))

        multivecupdater(vecarr,circarr,ind-1,arrang,arrfreq,tracker)

    else:
        vecarr[ind].add_updater(lambda m : m.move_to(ORIGIN + 0.5*vecarr[ind].get_complete_vector()))
        vecarr[ind].add_updater(lambda m : m.set_angle(arrang[ind]+arrfreq[ind]*tracker.get_value()))
        # circarr[ind].add_updater(lambda m : m.move_to(vecarr[ind-1].get_end()))
        # circarr[ind].add_updater(lambda m : m.move_to(vecarr[ind-1].get_end()))


vecarr = [[2,0,1],[1.5,PI/4,-1]]
rev_vecarr= vecarr[::-1]
print(rev_vecarr)
n = len(vecarr)

amp=[]
phang=[]
freq=[]

for i in range(n):
    amp.append(rev_vecarr[i][0])
    phang.append(rev_vecarr[i][1])
    freq.append(rev_vecarr[i][2])

class FourierVector(Vector):
    def get_complete_vector(self):
        return self.get_vector()
        
    def get_critical_point(self, direction):
        return (self.get_start() + self.get_end())/2
    

class AMLBGcam(Camera):
    CONFIG={
    "background_color": "#2457c4",
    }


class Fourier(Scene):
    CONFIG={
    "camera_class": AMLBGcam,
    }
    def construct(self):
        vecs = []
        circs = []
        # grid = ComplexPlane()
        VT = ValueTracker(0)

        multivecdefiner(amp,phang,vecs,circs,0)
        print(vecs[-1].get_end())

        multivecupdater(vecs,circs,len(vecs)-1,phang,freq,VT)
        print(vecs[-1].get_end())


        path = VMobject(color=WHITE)
        path.set_points_as_corners([vecs[-1].get_end(),vecs[-1].get_end()])
        # path.set_points_as_corners([vecs[-1].get_end(),vecs[-1].get_end()])

        path.add_updater(lambda m : m.append_vectorized_mobject(Line(path.points[-1],vecs[-1].get_end())))
        self.add(path)

        for x in range(len(amp)):
            self.add(vecs[x],circs[x])

        self.add(VT)
        VT.add_updater(lambda mobject, dt: mobject.increment_value(2*np.pi/100))
        self.wait(10)
