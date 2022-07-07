from manim import *
import numpy as np

#import files
v_proj_real = np.loadtxt('v_proj_real.dat')
v_proj_imag = np.loadtxt('v_proj_imag.dat')
phases = np.loadtxt('phases_numerical.dat')
phase_off = np.loadtxt('phase_off.dat')
r_num = np.loadtxt('r_numerical.dat')
time_linspace = np.loadtxt('time.dat')

time_step = 50 # 50
r_scale = 0.8

class Solution(Scene):
    def construct(self):
        ### normal factor
        norm = np.amax(np.sqrt(np.square(v_proj_real) + np.square(v_proj_imag)))
        # Equation
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{amsmath, bm}")
        equation = MathTex(
            "\\vec{x}(t) = \\underbrace{c_{1}\exp{(\lambda_{1}t)}}_{","\mu_{1}}","\\vec{v}_{1}",
            " + \\underbrace{c_{2}\exp{(\lambda_{2}t)}}_{","\mu_{2}}","\\vec{v}_{2}",
            " + \cdots + \\underbrace{c_{N}\exp{(\lambda_{N}t)}}_{","\mu_{N}}","\\vec{v}_{N}",
            tex_template=myTemplate
        )
        equation.set_color_by_tex('\mu_', RED)
        #animation
        self.play(Write(equation))
        self.wait(2)

        # Equation to Dots
        group2 = VGroup(Dot(7*LEFT,color=RED), Dot(6*LEFT,color=RED),Dot(5*LEFT,color=RED),
                        Dot(4*LEFT,color=RED), Dot(3*LEFT,color=RED),Dot(2*LEFT,color=RED),
                        Dot(LEFT, color=RED),  Dot(ORIGIN,color=RED),Dot(RIGHT, color= RED),
                        Dot(2 * RIGHT,color=RED), Dot(3 * RIGHT,color=RED), Dot(4 * RIGHT, color=RED),
                        Dot(5 * RIGHT, color=RED), Dot(6 * RIGHT,color=RED), Dot(7 * RIGHT,color=RED)
                        )

        #Animation
        self.play(
            Transform(equation, group2)
        )
        self.wait(0.5)

        ##### Constructing the planes
        ## 1 COMPLEX PLANE
        xlen = 6
        end = 1 #end points of axes
        plane = Axes(
            x_length=xlen,
            y_length=xlen,
            x_range=(-end, end),
            y_range=(-end, end),
            tips=False
        )
        plane.shift([3,0,0])

        x_label = MathTex("\\text{Real}").shift(plane.c2p(end + end/5, 0, 0)).scale(0.6)
        y_label = MathTex("\\text{Imaginary}").shift(plane.c2p(0, end + end/5, 0)).scale(0.6)
        circle = Circle(arc_center=plane.c2p(0, 0, 0), radius=3, color=WHITE)

        ## 2 R(t)
        axes_r = Axes(
            x_range=[0, 10, 0.5],
            y_range=[0, 1, 0.5],
            x_length=3,
            y_length=3,
            axis_config={"color": WHITE, "include_numbers": True},
            y_axis_config={
                "numbers_to_include": np.arange(0, 1.1, 1)
            },
            x_axis_config={
                "include_ticks": False,
                "numbers_to_include": np.arange(0, 10.1, 5)
            },
            tips=False
        )
        axes_r.shift([-4,2,0])
        # Labels for the axes
        labels_r = axes_r.get_axis_labels(
            x_label=MathTex("\\text{time} (s)").scale(0.6),
            y_label=MathTex("R(t)").scale(0.6)
        )

        ### Plot points
        graph = VGroup()
        for ii in range(len(r_num)):
            pt = Dot(axes_r.c2p(time_linspace[ii], r_num[ii], 0), color=WHITE, radius=0.025)
            graph.add(pt)

        ## 3 Phase Offset
        axes_po = Axes(
            x_range=[0, len(phases[0]), 1],
            y_range=[-PI, PI, 0.5],
            x_length=3,
            y_length=3,
            axis_config={"color": WHITE},
            y_axis_config={
                "include_ticks":False,
                "include_numbers":False
            },
            x_axis_config={
                "include_ticks": False,
                "numbers_to_include": np.arange(0, len(phases[0]) , 100),
                # "numbers_with_elongated_ticks": np.arange(0, 50, 10)
            },
            tips=False
        )
        axes_po.shift([-4,-2,0])
        # Labels for the axes
        labels_po = axes_po.get_axis_labels(
            x_label=MathTex("\\text{Oscillators}").scale(0.6),
            y_label=MathTex("\\text{Phase Offset}").scale(0.6)
        )

        po_y = VGroup(
            MathTex("\\pi", color=WHITE).next_to(axes_po.c2p(0, 3.14, 0), LEFT).scale(0.6),
            MathTex("-\\pi", color=WHITE).next_to(axes_po.c2p(0, -3.14, 0), LEFT).scale(0.6)
        )

        # # Initial t=0
        dots_initial = VGroup()
        dots_po_initial = VGroup()
        eig_mode_initial_r = v_proj_real[0, :]
        eig_mode_initial_i = v_proj_imag[0, :]
        py_initial = np.sin(phases[0])
        px_initial = np.cos(phases[0])

        for jj in range(len(eig_mode_initial_r)):
            dot_initial = Dot(plane.c2p(r_scale*(1/norm)*eig_mode_initial_r[jj], r_scale*(1/norm)*eig_mode_initial_i[jj], 0),radius= 0.05, color=RED)
            dot_phase_initial = Dot(plane.c2p(end*px_initial[jj] , end*py_initial[jj] ,0), color=GREEN)
            dots_initial.add(dot_initial, dot_phase_initial)

        for jj in range(len(phase_off[0])):
            dot_po = Dot(axes_po.c2p(jj, (phase_off[0])[jj], 0), color=GREY, radius=0.025)
            dots_po_initial.add(dot_po)

        # Legend
        dotrlegend = Dot(color=RED)
        rlegend = MathTex("\\mu_i ")
        dotglegend = Dot(color=GREEN)
        glegend = MathTex("\\theta_i")
        legend = VGroup(dotrlegend, rlegend, dotglegend, glegend).arrange_in_grid(rows=2).scale(0.7).to_corner(DOWN + RIGHT)

        # self.add( plane, circle,
        #           axes_po, labels_po, axes_r,
        #           labels_r, graph, dots_initial,
        #           legend, x_label, y_label, dots_po_initial, po_y
        # )

        self.play(
            Create(plane),
            Create(circle),
            Create(axes_po), Create(labels_po),
            Create(axes_r), Create(labels_r), Create(graph),
            ReplacementTransform(equation, dots_initial ),
            Create(x_label),
            Create(y_label),
            Create(legend),
            Create(dots_po_initial),
            Create(po_y)
        )

        self.wait(0.5)
        self.remove(dots_initial, dots_po_initial)

        #################################

        # The rest
        for kk in range(0, len(time_linspace), time_step):
            eig_mode_r = v_proj_real[kk, :]
            eig_mode_i = v_proj_imag[kk, :]
            dots_Red = VGroup()
            dots_Green = VGroup()
            py= np.sin(phases[kk])
            px = np.cos(phases[kk])

            for ii in range(len( eig_mode_r)):
                dot = Dot(plane.c2p(r_scale*(1/norm)*eig_mode_r[ii], r_scale*(1/norm)*eig_mode_i[ii], 0),radius= 0.05, color=RED)
                dot_phase = Dot(plane.c2p(end*px[ii], end*py[ii], 0), color=GREEN)
                dots_Red.add(dot)
                dots_Green.add(dot_phase)

            dots_po = VGroup()
            for jj in range(len(phase_off[kk])):
                dot_po = Dot(axes_po.c2p(jj, (phase_off[kk])[jj], 0), color=GREY,radius=0.025)
                dots_po.add(dot_po)

            t_label = axes_r.get_vertical_line(axes_r.c2p(time_linspace[kk], r_num[kk], 0), color=WHITE,stroke_width=5)

            time_var = MathTex( "t= {t:.2f}".format(t=0.001 * kk) )
            time_var.to_corner(UP+RIGHT)

            self.add(time_var)
            self.add(dots_Green)
            self.add(dots_Red)
            self.add(dots_po)
            self.add(t_label)
            self.wait(0.1)
            self.remove(t_label)
            self.remove(dots_po)
            self.remove(dots_Green)
            self.remove(dots_Red)
            self.remove(time_var)

        self.wait(0.3)


