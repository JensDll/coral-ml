using Application.Data.Models;
using Contracts.Request;
using Contracts.Response;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Data.Repositories
{
    public interface IModelRepository
    {
        public Task<EnumerableEnvelopeDto<TFLiteModelGetAllDto>>
            GetAllAsync(PaginationRequestDto paginationRequest);

        public Task<byte[]> GetByIdAsync(int id);

        public Task<int> CreateAsync(IFormFile model);

        public Task<int> DeleteAsync(int id);
    }
}
