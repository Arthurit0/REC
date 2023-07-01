import asyncio

async def start_iperf_server(protocol):
    command = f"iperf3 -s -p {port}"
    port = port + 1
    with open(f'{protocol}_server_output.txt', 'w') as f:
        process = await asyncio.create_subprocess_exec(
            *command.split(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        print(f"Started iperf3 {protocol.upper()} server on port {port} [PID: {process.pid}]")
        while True:
            output = await process.stdout.readline()
            if output == b'' and process.stdout.at_eof():
                break
            f.write(output.decode())
    return process

async def main():
    port = 5201


    # bitrate = input('Insira o bitrate para o servidor udp: ')
    udp_server = await start_iperf_server('udp')
    tcp_server = await start_iperf_server('tcp')

    await asyncio.gather(
        tcp_server.communicate(),
        udp_server.communicate()
    )

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Servers stopped by user")
    for child in asyncio.all_tasks():
        child.cancel()
