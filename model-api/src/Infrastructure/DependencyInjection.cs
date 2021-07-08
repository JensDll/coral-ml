using Application.Data;
using Application.Data.Repositories;
using Application.Data.Services;
using Infrastructure.Data;
using Infrastructure.Data.Repositories;
using Infrastructure.Data.Services;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using System.Text.Json;

namespace Infrastructure
{
    public static class DependencyInjection
    {
        public static void AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
        {
            // data access
            services.AddSingleton<IConnectionFactory>
                (new ConnectionFactory(configuration.GetConnectionString("ModelDb")));
            services.AddSingleton<IModelRepository, ModelRepository>();
            services.AddSingleton<IPaginationService, PaginationService>();
        }
    }
}
