dp.Report(
        dp.Blocks(
            dp.Plot(fig0),
            dp.Plot(fig1),
            dp.Plot(fig2),
            dp.Plot(fig3),
            dp.Plot(fig4),
            dp.Plot(fig5),
            dp.Plot(fig6),
            dp.Plot(fig7),
            columns=2,
            rows=4
        ), dp.Plot(fig8)
    ).publish(name='stock_report', open=True)