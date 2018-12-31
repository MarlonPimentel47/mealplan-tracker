from plotly.graph_objs import Scatter
from plotly.offline import plot


#  y_data is list of field data only (gotten from each record)
def test_graph(records):
    y_data = []
    x_data = []
    for record in records:
        date = record.date.strftime("%m/%d %X")
        avg = record.money_spent
        y_data.append(record.net_cash)
        x_data.append('{},${}'.format(date, avg))

    my_plot_div = plot([Scatter(x=x_data[::-1],
                                y=y_data[::-1],
                                name="Rollover $/Own $ To Add",
                                marker=dict(
                                    color='rgb(116,175, 173)',
                                    line=dict(
                                        color='rgb(116, 175, 173)'
                                    )
                                )
                                )],
                       output_type='div')
    return my_plot_div

