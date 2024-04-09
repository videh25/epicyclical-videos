from big_ol_pile_of_manim_imports import*

scale_factor = 1

def multivecupdater(arr,circarr,ind,arrang,arrfreq,tracker):
    if ind>0:
        arr[ind].add_updater(lambda m : m.move_to(arr[ind-1].get_end()+ 0.5*arr[ind].get_vector()))
        arr[ind].add_updater(lambda m : m.set_angle(arrang[ind]+arrfreq[ind]*tracker.get_value()))
        circarr[ind].add_updater(lambda m : m.move_to(arr[ind-1].get_end()))

        multivecupdater(arr,circarr,ind-1,arrang,arrfreq,tracker)

    else:
        arr[ind].add_updater(lambda m : m.set_angle(arrang[ind]+arrfreq[ind]*tracker.get_value()))
class AMLBGcam(Camera):
    CONFIG={
    "background_color": "#2457c4",
    }

class tempo(Scene):
     CONFIG={
    "camera_class": AMLBGcam,
    }
    def construct(self):
        import numpy
        filename = 'Vectors.csv'
        raw_data = open(filename, 'rt')
        data = numpy.loadtxt(raw_data, delimiter=",")
        freq = []
        ampli = []
        phase = []

        for row in data:
            ampli.append(row[0])
        for row in data:
            phase.append(row[1])
        for row in data:
            freq.append(row[2])
        m = len(ampli)

        VT = ValueTracker(0)
        vector = []
        circle = []
        for n in range(m):
            vector.append(Vector(np.array([ampli[n],0,0] )/scale_factor,color = WHITE  ))
            circle.append(Circle(radius = ampli[n], stroke_w/scale_factor,width=0.25, color=WHITE))

        multivecupdater(vector,circle,len(vector)-1,phase,freq,VT)

        for i in range(m):
            self.add(vector[i],circle[i])

        self.play(
            VT.set_value,2*PI,
            rate_func=linear,
            run_time=8,
                 )
        self.wait(1)
