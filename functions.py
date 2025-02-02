from graph import *
from settings import *


def convert_to_csv(file):
    """
        Converts .xls and .xlsx files to .csv files
        :param file: path to file
        :return: saves image to temp/{file_id}.png
    """
    if file.filename.endswith('.xlsx'):
        file.attachments[0].save('temp/file.xlsx')
        file = pandas.read_excel('temp/file.xlsx')
        file.to_csv('temp/file.csv')
    elif file.filename.endswith('.xls'):
        file.attachments[0].save('temp/file.xls')
        file = pandas.read_excel('temp/file.xls')
        file.to_csv('temp/file.csv')


async def wait_for_message(ctx):
    """
        Asynchronously waits for message then returns message if message sent
        :param ctx: bot context
        :return: message if message sent, else None
    """
    try:
        msg = await bot.wait_for('message', timeout=60)
    except asyncio.TimeoutError:
        await ctx.send('Timed out. Please try again.')
        return None
    else:
        return msg


async def check_graph_type(ctx, max_val):
    """
        Waits for user input then returns information
        :param ctx: bot context
        :param max_val: max acceptable value
        :return: an integer that corresponds to expected graph type
    """
    msg = await wait_for_message(ctx)
    if msg:
        msg = msg.content
        if not msg.isnumeric():
            await ctx.send("Graph type must be inputted as an integer. Please try again.")
            return -1
        if not float(msg).is_integer():
            await ctx.send("Graph type must be inputted as an integer. Please try again.")
            return -1
        msg = int(msg)
        if msg <= 0 or msg > max_val:
            await ctx.send("Invalid graph type")
            return -1
        return msg
    return -1


def verify_data(data: list, row_len: int, col_len: int) -> bool:
    """
        Verifies that the contents of the .csv file are all numeric
        :param data: user inputted data
        :param row_len: numer of rows
        :param col_len: numer of columns
        :return: boolean of whether data is valid or not
    """
    if all([len(data[i]) == col_len for i in range(row_len)]):
        x = [[data[i][j] for j in range(col_len)] for i in range(1, row_len)]
        x = reduce(lambda a, b: a + b, x)
        x = [i.isnumeric() for i in x]
        return all(x)
    return False


async def initial_analysis(ctx, file_path, file_id):
    """
        Analyzes data and sends image back to user
        :param ctx: bot context
        :param file_path: path to data file
        :param file_id: file id
        :return: saves image to temp/{file_id}.png
    """
    with open(file_path, 'r') as data:
        data = list(csv.reader(data))
        row_len = len(data)
        if row_len <= 1:
            await ctx.send("Data invalid. Please run `d!help` for more information "
                           "on formatting your data for graphing")
            return
        col_len = len(data[0])
        if not verify_data(data, row_len, col_len):
            await ctx.send("Data invalid. Please run `d!help` for more information "
                           "on formatting your data for graphing")
            return
        if row_len == 2:
            await ctx.send("Please choose a graph type: Pie (1)")
            x = await check_graph_type(ctx, 1)
            if x == 1:
                basic_pie(file_path, file_id)
        else:
            if col_len == 2:
                await ctx.send("Please choose a graph type: X vs Y *line* (1), X vs Y *scatter* (2), "
                               "X vs Y *bar* (3)")
                x = await check_graph_type(ctx, 3)
                if x == 1:
                    two_var_line(file_path, file_id)
                elif x == 2:
                    two_var_scatter(file_path, file_id)
                elif x == 3:
                    two_var_bar(file_path, file_id)
                else:
                    return
            elif col_len == 3:
                await ctx.send("Please choose a graph type: X vs Y1 vs Y2 *line* (1), X vs Y vs Y2 *scatter* (2), "
                               "X vs Y1 vs Y2 *bar* (3)")
                x = await check_graph_type(ctx, 2)
                if x == 1:
                    three_var_line(file_path, file_id)
                elif x == 2:
                    three_var_scatter(file_path, file_id)
                # elif x == 3:
                #     two_var_bar(file_path, file_id)
                else:
                    return
        file = open('temp/{0}.png'.format(file_id), 'rb')
        await ctx.send(file=discord.File(file, '{0}.png'.format(file_id)))
        file.close()

