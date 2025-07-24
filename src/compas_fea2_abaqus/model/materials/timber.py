from compas_fea2.model.materials.timber import Timber


class AbaqusTimber(Timber):
    """"""

    __doc__ += Timber.__doc__

    def __init__(
        self,
        fmk,
        ft0k,
        fc0k,
        ft90k,
        fc90k,
        fvk,
        vLT,
        vTT,
        E0mean,
        E90mean,
        Gmean,
        densityk,
        density,
        **kwargs,
    ):
        super().__init__(
            fmk,
            ft0k,
            fc0k,
            ft90k,
            fc90k,
            fvk,
            vLT,
            vTT,
            E0mean,
            E90mean,
            Gmean,
            densityk,
            density,
            **kwargs,
        )

    # def jobdata(self):
    #     return AbaqusElasticOrthotropic(Ex=self.Ex, Ey=self.Ey, Ez=self.Ez, vxy=self.vxy, vyz=self.vyz, vzx=self.vzx, Gxy=self.Gxy, Gyz=self.Gyz, Gzx=self.Gzx,
    #                                     density=self.density, name=self.name).jobdata()

    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """
        jobdata = [f"*Material, name={self.name}"]

        if self.density:
            jobdata.append(f"*Density\n{self.density},")

        jobdata.append(
            f"*Elastic, type=ENGINEERING CONSTANTS\n{self.Ex}, {self.Ey}, {self.Ez}, {self.vxy}, {self.vzx}, {self.vyz}, {self.Gxy}, {self.Gzx}\n {self.Gyz},"
        )
        if self.expansion:
            jobdata.append("*Expansion\n{},".format(self.expansion))
        jobdata.append("**")
        return "\n".join(jobdata)
