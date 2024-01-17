import dash
from dash import html, dcc, Input, Output, State
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go
from nii_skeletonizin import get_data

coords = get_data("/Users/mrniu/Desktop/data/1-200/90.label.nii.gz")

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='3d-scatter-plot',
        figure=go.Figure(
            data=go.Scatter3d(
                x=coords[0],
                y=coords[1],
                z=coords[2],
                mode='markers',
                marker=dict(size=5, color='blue')
            ),
            layout=go.Layout(title='3D Scatter Plot', clickmode='event+select')
        ),
        style={'width': '100%', 'height': '80vh'}  #将宽度设置为视口高度的100%，将高度设置为视口高的80%
    ),
    html.Pre(id='selected-coords'),  # 用于显示选中的坐标
    html.Div(id='status-message'),   # 用于显示状态信息
    html.Button('Delete Last Selected Point', id='delete-button')  # 用于删除最后一个选中的点
])
selected_coords = []
data_clicks_count = 0
n_click_count = 0
@app.callback(
    [Output('selected-coords', 'children'),
     Output('status-message', 'children')],
    [Input('3d-scatter-plot', 'clickData'),
     Input('delete-button', 'n_clicks')]
)
def save_and_display_click_data(clickData, n_clicks):
    ctx = dash.callback_context
    global selected_coords
    global data_clicks_count
    global n_click_count
    num = 20

    if not ctx.triggered:
        return ('', 'Click to select points.')
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        

        if trigger_id == '3d-scatter-plot':
            if len(selected_coords) >= num:
                return ('\n'.join(map(str, selected_coords)), '20 points have been selected and saved to a file.')
            point = clickData['points'][0]
            coord = (point['x'], point['y'], point['z'])
            selected_coords.append(coord)

            # 选中num个点后保存到文件
            if len(selected_coords) == num:

                coords_array = np.array(selected_coords).reshape(1, num, 3)
                np.save('selected_coords.npy', coords_array)
                return ('\n'.join(map(str, selected_coords)), '20 points have been selected and saved to a file.')

        if trigger_id == 'delete-button':
            try:
                selected_coords.pop()
            except Exception as e:
                print(f'Exception: {e}')
            coords_display = '\n'.join(map(str, selected_coords))
            return (coords_display, f'{len(selected_coords)} points selected. Click to select more points.')

    coords_display = '\n'.join(map(str, selected_coords))
    return (coords_display, f'{len(selected_coords)} points selected. Click to select more points.')

if __name__ == '__main__':
    app.run_server(debug=True)