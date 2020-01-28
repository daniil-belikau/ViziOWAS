from vizutil import data
from vizutil import plot

def run(args):

    df = data.data_import(args.input_path, args.separation_strategy)
    df = data.data_clean(df, [args.x_axis, args.y_axis, args.group], args.y_axis)
    df = data.format_yaxis(df, args.y_axis, args.association_var)

    hover_data = plot.assemble_hover_data(args.hover_data)

    bonferroni_threshold = data.bonferroni(df, args.y_axis)
        
    if args.ancol:
        manual = False
        threshold = args.ancol
    else: 
        manual = True
        threshold = bonferroni_threshold
    
    if args.neg:
        lines = [(bonferroni_threshold, 'red'), (-bonferroni_threshold, 'red'), (0, 'lightgrey')]
    else:
        lines = [(bonferroni_threshold, 'red'), (0, 'lightgrey')]
        
    annotations = data.create_annotations(df, args.x_axis, args.y_axis, args.anvar, threshold, args.anlim, manual)
    
    df = data.transform_hover_data(df, hover_data[2])

    fig = plot.produce_figure(df, args.x_axis, args.group, hover_data[0])
    fig = plot.customize_markers(fig, df[args.group].unique(), args.group, hover_data[1], args.marker_size, args.crowded_origin)
    fig = plot.customize_layout(fig, args.title, annotations, args.x_axis, args.show_legend, df[args.x_axis].max(), lines, args.association_var, True)
    
    plot.export_plot(fig, args.output_path, args.output_formats, args.width, args.height)
