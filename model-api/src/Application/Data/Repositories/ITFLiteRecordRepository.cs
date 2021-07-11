using Application.Data.Models;
using Contracts.Request;
using Contracts.Response;
using Domain.DataTransfer;
using Domain.Entities;
using Domain.ValueObjects;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Data.Repositories
{
    public interface ITFLiteRecordRepository
    {
        public Task<EnumerableEnvelope<TFLiteRecordModel>> GetAllAsync(Pagination pagination);

        public Task<byte[]> GetByIdAsync(int id);

        public Task<int> CreateAsync(string modelName, FormFileZipper zipper);

        public Task<int> DeleteAsync(int id);
    }
}
