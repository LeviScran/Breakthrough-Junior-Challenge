# This was an animation rendering for the Breakthrough Junoir Challenge
# which I submitted this summer.
#
# My submission can be viewed at: https://www.youtube.com/watch?v=_GMq5HSFY44.
#
# Uses Manim Community software (originally created by
# Grant Sanderson of 3Blue1Brown) to render.
#
# The double pendulum simulation was adapted from
# Physics Explained on YouTube, original code can be viewed at
# https://trinket.io/glowscript/7069d44ff5.





from manim import *
import numpy as np

class Pendulum2(MovingCameraScene):
    def construct(self):

        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")

        def directions(angle, distance):
            return distance * UP * np.sin(angle) + distance * LEFT * np.cos(angle)

        point = Circle(radius=.03, color=BLUE).shift(UP*3)
        bob = Circle(radius=.4, color=BLUE, fill_color=BLACK, fill_opacity=1).shift(DOWN*1)
        text = Text("The Simple Pendulum").to_edge(DOWN)
        connection = always_redraw(lambda : Line(point.get_center(), bob.get_center(), color=BLUE, buff=0))

        self.play(Create(VGroup(point, bob, connection, text)))
        self.add_foreground_mobjects(point, bob)

        self.bring_to_back(connection)
        self.wait()
        self.play(Rotate(bob, angle=PI/8, about_point=point.get_center(), rate_func=rate_functions.ease_in_out_sine, run_time=1.29))

        for i in range(3):
            self.play(Rotate(bob, angle=-PI / 4, about_point=point.get_center(), rate_func=rate_functions.ease_in_out_sine, run_time=1.29))
            self.play(Rotate(bob, angle=PI/4, about_point=point.get_center(), rate_func=rate_functions.ease_in_out_sine, run_time=1.29))
        self.play(Uncreate(text))
        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.set(width=bob.width * 10).move_to(bob))
        self.wait(.5)


        arrowMain = Arrow(bob.get_center() + DOWN * .4, bob.get_center() + DOWN * 1.9, buff=.05, color=WHITE, max_tip_length_to_length_ratio=.15)
        arrowX = Arrow(bob.get_center() + directions(-PI/8, .4), bob.get_center() + directions(-PI/8, 1.9 * np.sin(PI/8)), buff = .05)
        arrowY = Arrow(bob.get_center() + directions(-PI * 5/8, .4), bob.get_center() + directions(-PI * 5/8, 1.9 * np.cos(PI/8)), buff=.05,  max_tip_length_to_length_ratio=.15)
        self.play(Create(VGroup(arrowMain)))
        self.wait(1)
        mainFont = 50
        text = MathTex("F = -mg", font_size=mainFont).scale(.5).next_to(arrowMain)
        self.play(Create(VGroup(text)))
        self.wait(1)


        self.play(text.animate.shift(RIGHT))
        dashedX = DashedLine(bob.get_bottom() + DOWN * 1.5, bob.get_center() + directions(-PI/8, 1.9 * np.sin(PI/8)), stroke_width=3)
        dashedY = DashedLine(bob.get_bottom() + DOWN * 1.5, bob.get_center() + directions(-PI * 5/8, 1.9 * np.cos(PI/8)), stroke_width=3)

        self.play(Create(VGroup(dashedX, dashedY, arrowX, arrowY)))
        self.wait(.5)
        #self.wait(.5)
        self.play(Uncreate(arrowMain), Uncreate(text), Uncreate(dashedY), Uncreate(dashedX))
        text1 = MathTex(r"F = -mgsin(\theta)", font_size=mainFont).next_to(arrowX).shift(DOWN * .4 + LEFT * 2.5).scale(.5)
        text2 = MathTex(r"F = -mgcos(\theta)", font_size=mainFont).next_to(arrowY).shift(LEFT).scale(.5)
        #self.play()

        rotation_center = bob.get_center() + directions(PI * 3 / 8, 2)

        theta_tracker = ValueTracker(-1)
        line1 = Line(rotation_center, rotation_center - directions(PI * 3 / 8, 1), color=BLUE)
        line_moving = Line(rotation_center, rotation_center - directions(PI * 3 / 8, 1))#, color=BLUE)
        line_ref = line_moving.copy()
        line_moving.rotate(
            theta_tracker.get_value() * DEGREES, about_point=rotation_center
        )
        a = Angle(line_moving, line1, radius=0.5, other_angle=False, color=BLUE)
        tex = Text("θ", font_size= 12).move_to(
            Angle(
                line_moving,line1, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5)
        )
        self.add(line1, line_moving, a, tex)

        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center
            )
        )

        a.add_updater(
            lambda x: x.become(Angle(line_moving, line1, radius=0.5, other_angle=False))
        )
        tex.add_updater(
            lambda x: x.move_to(
                Angle(
                    line_moving, line1, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
                ).point_from_proportion(0.5)
            )
        )
        self.remove(Uncreate(text))

        self.play(theta_tracker.animate.set_value(-180/8),Create(VGroup(text1, text2)))


        self.wait(1.5)

        self.play(Uncreate(text2), Uncreate(arrowY), Uncreate(arrowX))
        self.remove(line1, line_moving, a, tex)
        self.play(Restore(self.camera.frame))

        self.play(text1.animate.move_to(DOWN * 3 + RIGHT * 1).scale(2))

        self.wait(2)
        textTrans1 = MathTex(r"F = ma", font_size=mainFont).move_to(DOWN * 3 + LEFT * 3)
        textTrans2 = MathTex(r"ma = -mgsin(\theta)", font_size=mainFont).move_to(DOWN * 3)
        textTrans3 = MathTex(r"a = -gsin(\theta)", font_size=mainFont).move_to(DOWN * 3)
        textTrans31 = MathTex(r"a = -g\theta", font_size=mainFont).move_to(DOWN * 3)
        textTrans4 = MathTex(r"\frac{d^2\theta}{dt^2} l = -g\theta", font_size=mainFont).move_to(DOWN * 3)
        textTrans4 = MathTex(r"\frac{d^2\theta}{dt^2} = -\frac{g}{l}\theta", font_size=mainFont).move_to(DOWN * 3)
        addEq = MathTex(r"w = \sqrt{\frac{g}{l}}", font_size=mainFont).move_to(DOWN * 2 + RIGHT * 3)
        textTrans5 = MathTex(r"\theta = c_1 cos(wt) + c_2 sin(wt)", font_size=mainFont).move_to(DOWN * 3)
        threeReplacements = VGroup(MathTex(r"C = \sqrt{c_1^2 + c_2^2}", font_size=mainFont), MathTex(r"cos(\alpha) = \frac{c_2}{C}", font_size=mainFont), MathTex(r"sin(\alpha) = -\frac{c_1}{C}", font_size=mainFont)).arrange_in_grid(rows=3, buff=.2).move_to(DOWN + LEFT * 2)
        niceSine = MathTex(r"\theta = C sin(w t - \alpha)", font_size=mainFont).move_to(DOWN * 3)
        self.play(Create(VGroup(textTrans1)))
        self.wait(1)

        self.play(Transform(mobject=text1, target_mobject=textTrans2), Uncreate(VGroup(textTrans1)))
        self.play(text1.animate.move_to(DOWN * 3))
        self.wait(1)
        self.play(Transform(mobject=text1, target_mobject=textTrans2))
        self.wait(.5)

        self.play(Transform(mobject=text1, target_mobject=textTrans3))
        self.wait(3)
        self.play(Transform(mobject=text1, target_mobject=textTrans31))
        self.wait(1)
        self.play(Transform(mobject=text1, target_mobject=textTrans4))
        self.play(Create(VGroup(addEq)))
        self.wait(1)
        self.play(text1.animate.move_to(DOWN*2))
        self.play(Create(VGroup(textTrans5)))
        self.wait(1)
        self.play(Uncreate(text1), Uncreate(addEq))
        self.play(Create(VGroup(threeReplacements)))
        self.wait(1)
        self.play(Transform(textTrans5, niceSine), Uncreate(threeReplacements))
        self.wait(2)
        self.play(point.animate.shift(RIGHT * 2), bob.animate.shift(RIGHT * 2))

        ax = Axes(x_range=[0, 4*PI, PI], y_range=[-1.5, 1.5]).scale(.4).shift(LEFT * 3)
        graph = ax.plot(lambda x: np.sin(x) / 3, color=BLUE, x_range=[0, 3 * PI])
        moving_dot = Dot(ax.i2gp(graph.t_min, graph), color=ORANGE)
        self.add(ax, graph, moving_dot)

        def update_pendulum(bob):
            dt = 1/30
            amplitude = .5
            t = self.t

            theta = -moving_dot.get_center()[1] * 2
            bob.move_to(rotate_vector(4 * DOWN, theta) + point.get_center())
            self.t += dt

        pendulum_updater = UpdateFromFunc(bob, update_pendulum)
        # Initialize time
        self.t = 0
        self.play(Rotate(bob, angle=-PI / 8, about_point=point.get_center(), rate_func=rate_functions.ease_in_sine, run_time=1))
        self.play(MoveAlongPath(moving_dot, graph, rate_func=linear, run_time=4),pendulum_updater)
        self.remove(pendulum_updater)
        self.wait(1)
        graph2 = ax.plot(lambda x: np.sin(x) * 1.5, color=BLUE, x_range=[0, 3 * PI])
        self.play(Transform(graph, graph2))
        self.play(MoveAlongPath(moving_dot, graph, rate_func=linear, run_time=4), pendulum_updater)
        self.remove(pendulum_updater)
        self.wait(1)

        aproximation = MathTex(r"a = -g sin(\theta)", r"\approxeq -g \theta").move_to(DOWN * 3)

        self.play(Uncreate(graph), Uncreate(ax), Uncreate(moving_dot), Uncreate(textTrans5))
        self.play(Create(VGroup(aproximation)))
        self.wait(2)
        ax = Axes(x_range=[-6, 6], y_range=[-1.5, 1.5]).scale(.6).shift(LEFT * 3)
        graph3 = ax.plot(lambda x: np.sin(x), color=BLUE, x_range=[-5, 5])
        graph4 = ax.plot(lambda x: x, color=RED, x_range=[-1.5, 1.5])
        lableOne = MathTex(r"y = x", color=RED, font_size=35).move_to(LEFT * 2 + DOWN * 1.4)
        lableTwo = MathTex(r"y = sin(x)", color=BLUE, font_size=35).move_to(LEFT * 2 + DOWN * 1)
        self.play(Create(VGroup(ax, graph3, graph4, lableOne, lableTwo), run_time=1.5))
        self.play(self.camera.frame.animate.set(width=ax.width*1.2).move_to(ax))
        rectangle1 = Rectangle(height=1, width=.6).move_to(ax.get_center())
        framebox1 = SurroundingRectangle(rectangle1, buff=.1)
        self.play(Create(VGroup(framebox1)))
        self.wait(2)
        self.play(Uncreate(framebox1))
        self.play(Restore(self.camera.frame))

        realApp = MathTex(r"a = -g sin(\theta)", font_size=mainFont).move_to(DOWN * 3)

        self.play(ReplacementTransform(aproximation, realApp))

        self.wait(2)

        textTrans7 = MathTex(r"\frac{d^2\theta}{dt^2} = -\frac{g}{l} sin(\theta)", font_size=mainFont).move_to(DOWN * 3)

        self.play(ReplacementTransform(realApp, textTrans7))

        self.play(Uncreate(ax), Uncreate(graph4), Uncreate(graph3), Uncreate(lableTwo), Uncreate(lableOne))

        self.play(textTrans7.animate.move_to(LEFT * 3 + UP * 2.5).scale(.7), point.animate.shift(RIGHT * 2), bob.animate.shift(RIGHT * 2))
        self.wait(2)
        ellipiticInt = MathTex(r"\theta (t) = 2 arcsin\left(k * cd\left(\sqrt{\frac{g}{l}}t; k\right) \right)", font_size=mainFont).move_to(LEFT * 3 + UP).scale(.7)
        kVal = MathTex(r"k = sin\left(\frac{\theta_0}{2}\right)").next_to(ellipiticInt).shift(RIGHT * .4).scale(.7)
        self.play(Create(VGroup(ellipiticInt, kVal)))
        self.wait(2)

        eq1 = MathTex(r"am(u, m) = \phi", font_size=mainFont).move_to(LEFT * 4 + DOWN * 1.5).scale(.7)
        intagral = MathTex(r"u = \int_{0}^{\phi} \frac{d\theta}{\sqrt{1-m sin^2(\theta)", font_size=mainFont).scale(.7).next_to(eq1, buff= .5)

        eq4 = MathTex(r"cd(u) = \frac{cn(u)}{dn(u)}", font_size=mainFont).move_to(LEFT * 6 + DOWN *.25).scale(.6)
        eq3 = MathTex(r"dn(u, m) = \frac{d}{du} am(u, m)", font_size=mainFont).scale(.6).next_to(eq4, buff= .5)

        qe2 = MathTex(r"cn(u, m) = cos(am(u, m))", font_size=mainFont).scale(.6).next_to(eq3, buff= .5)

        # Maybe add picture of ellipse that repersents cd
        # Remeber cd = cn / dn = (x/a)/(r/a) = x/r
        self.play(Create(VGroup(eq1, qe2, eq3, eq4, intagral)))

        self.wait(4.5)

        self.play(Uncreate(ellipiticInt), Uncreate(ellipiticInt), Uncreate(textTrans7), Uncreate(kVal), Uncreate(eq1), Uncreate(qe2), Uncreate(eq3), Uncreate(eq4), Uncreate(intagral))

        self.play(bob.animate.move_to(rotate_vector(DOWN * 2.5, PI/2) + UP * 2).scale(.7), point.animate.move_to(UP * 2))
        self.wait()
        bob2 = Circle(radius=.4, color=BLUE, fill_color=BLACK, fill_opacity=1).move_to(rotate_vector(DOWN * 2.5, PI * .5 + 1) + bob.get_center()).scale(.7)


        self.add_foreground_mobjects(bob2)

        connection2 = always_redraw(lambda : Line(bob2.get_center(), bob.get_center(), color=BLUE, buff=0))
        self.play(Create(VGroup(connection2, bob2)))
        global theta1
        global theta2
        global theta1dot
        global theta2dot
        global dt
        dt = 1/30
        theta1 = PI/2
        theta2 = PI/2 + 1
        theta2dot = 0
        theta1dot = 0


        def updatePendBottom(bob):
            global theta1
            global theta2
            global theta2dot
            global theta1dot
            g = 1
            M1 = 1
            M2 = 1
            R1 = 1
            R2 = 1
            a = -(M1 + M2) * g * R1 * np.sin(theta1) - M2 * R1 * R2 * theta2dot ** 2 * np.sin(theta1 - theta2)
            b = (M1 + M2) * R1 ** 2
            c = M2 * R1 * R2 * np.cos(theta1 - theta2)
            f = -M2 * g * R2 * np.sin(theta2) + M2 * R1 * R2 * theta1dot ** 2 * np.sin(theta1 - theta2)
            k = M2 * R2 ** 2
            w = M2 * R1 * R2 * np.cos(theta1 - theta2)
            theta2ddot = (f - a * w / b) / (k - c * w / b)
            theta1ddot = a / b - c * theta2ddot / b
            theta2dot = theta2dot + theta2ddot * dt
            theta1dot = theta1dot + theta1ddot * dt
            theta1 = theta1 + theta1dot * dt
            theta2 = theta2 + theta2dot * dt
            #t = t + dt
            bob.move_to(rotate_vector(2.5 * DOWN, theta1) + point.get_center())
            bob2.move_to(rotate_vector(2.5 * DOWN, theta2) + bob.get_center())


        self.play(UpdateFromFunc(bob, updatePendBottom), run_time=15)













if __name__ == "__main__":
    scene = Pendulum2()
    scene.render()
