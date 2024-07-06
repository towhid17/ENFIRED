from algo.DSLoadBalancer import DSLoadBalancer
from algo.RoundRobinLoadBalancer import RoundRobinLoadBalancer
from algo.LeastLinkUtilization import LeastLinkUtilization
from algo.NearestFog import NearestFog
from algo.WDSLoadBalancer import WDSLoadBalancer


class LoadBalancerFactory:
    @staticmethod
    def create_load_balancer(algorithm, net_info):
        if algorithm == 'enfired':
            return DSLoadBalancer(net_info)
        elif algorithm == 'rr':
            return RoundRobinLoadBalancer(net_info)
        elif algorithm == 'llu':
            return LeastLinkUtilization(net_info)
        elif algorithm == 'nf':
            return NearestFog(net_info)
        elif algorithm == 'enfired_lite':
            return WDSLoadBalancer(net_info)
        else:
            raise ValueError("Unsupported load balancing algorithm")
